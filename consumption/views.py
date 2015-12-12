# -*- coding: utf-8 -*-
from django.db.models import Avg

from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateView
# from consumption.forms import UploadFileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import messages

from equipment.models import Equipment
from consumption.models import Consumption
from aes_rate.models import AESRate
from goal.models import Goal
from consumption.models import Consumption
from sensor.models import Sensor

from django.template import RequestContext
from datetime import datetime, timedelta
import unicodecsv
import csv
import json
import ast
import traceback
from django.db import connection
import calendar
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from pytz import NonExistentTimeError
from exceptions import ValueError
from collections import defaultdict

class GraphicView(TemplateView):
	# form_class = UploadFileForm
	template_name = "consumption/graphic.html"
	# form = UploadFileForm()

	def get_context_data(self, **kwargs):
		context = super(GraphicView, self).get_context_data(**kwargs)
		user = self.request.user

		if hasattr(user, 'profile'):
			context["income_type"] = user.profile.income_type

		context["measurement_units"] = Equipment.MEASUREMENT_UNITS
		context["months"] = ((1, "Janeiro"),(2, "Fevereiro"),(3, "Março"),(4, "Abril"),(5, "Maio"),(6, "Junho"),(7, "Julho"),(8, "Agosto"),(9, "Setembro"),(10, "Outubro"),(11, "Novembro"),(12, "Dezembro"))
		context["equipments"] = Equipment.objects.all()
		return context

def get_first_day_of_month(dt, d_years=0, d_months=0):
	# d_years, d_months are "deltas" to apply to dt
	y, m = dt.year + d_years, dt.month + d_months
	a, m = divmod(m-1, 12)
	return datetime(y+a, m+1, 1)

def get_last_day_of_month(dt):
	return get_first_day_of_month(dt, 0, 1) + timedelta(-1)

# Parâmetros usados:
	# code: código do sensor
	# voltage: medida de voltagem
	# current: corrente medida
def create(request):
	try:
		if request.method == 'POST':
			# consumption = "{'voltage': 5.32, 'current': 1.23}"
			consumption = request.POST.get('consumption')
			consumption_params = ast.literal_eval(consumption)
			code = request.POST.get("code").encode("utf-8")
			current = consumption_params.get("i", -1.0)
			voltage = consumption_params.get("v", -1.0)

			sensor = None

			existing_sensor = Sensor.objects.filter(code=code)

			if existing_sensor.count() > 0:
				sensor = Sensor.objects.filter(code=code).first()
			else:
				sensor = Sensor.objects.create(code=code, name="sensor_" + code)
				sensor.save()

			equipment = sensor.equipment

			if current > 0:
				if voltage > 0:
					Consumption.new(datetime.now(), current, voltage, equipment.id).save()

			return HttpResponse(status=201)
		else:
			return HttpResponse(status=404)
	except Exception as e:
		traceback.print_exc()
		return HttpResponse(status=500)

def importCSV(request):
	if request.method == 'POST': # If the form has been submitted...
		# form = UploadFileForm(request.POST) # A form bound to the POST data
		# if form.is_valid(): # All validation rules pass
		lineNumber = 0
		try:
			csv_imported = request.FILES['csv']
			csv_imported.open()
			csv_reader = unicodecsv.DictReader(csv_imported, lineterminator = '\n', delimiter=';', encoding='UTF-8')
			with transaction.atomic():
				for line in csv_reader:
					lineNumber += 1
					Consumption.new(line['moment'], line['current'], line['voltage'], line['equipment_id']).save()
			url = reverse('consumption:graphic')
			return HttpResponseRedirect(url)

		except ValidationError as e:
			url = reverse('consumption:graphic')
			messages.error(request, "Linha " + str(lineNumber) + ": " + '; '.join(e.messages))
			return HttpResponseRedirect(url)

		except MultiValueDictKeyError as e2:
			url = reverse('consumption:graphic')
			messages.error(request, "Escolha um arquivo para fazer a importação.")
			return HttpResponseRedirect(url)

		except ValueError as e3:
			url = reverse('consumption:graphic')
			
			messages.error(request, "Linha "  + str(lineNumber) + ": " + str(e3))
			return HttpResponseRedirect(url)

		except NonExistentTimeError as e4:
			url = reverse('consumption:graphic')
			
			messages.error(request, "Horário inexistente na linha "  + str(lineNumber) + ": " + line['moment'])
			return HttpResponseRedirect(url)

def exportCSV(request):
	if request.method == 'GET':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="report.csv"'
		response.write(u'\ufeff'.encode('utf8'))
		fieldnames = ['moment', 'current', 'voltage', 'equipment_id']
		writer = csv.DictWriter(response, delimiter=";", fieldnames=fieldnames)

		consumption_report = Consumption.objects.order_by('equipment_id', 'moment')
		writer.writeheader()
		for consumption in consumption_report:
			writer.writerow(
				{
				'moment': consumption.moment, 
				'current': consumption.current, 
				'voltage': consumption.voltage, 
				'equipment_id': consumption.equipment_id
				}
			)
		return response

# IN:
# 	goal (true/false)
# 	timeRange (daily/hourly/monthly)
# 	unit (w/kw)
# 	xStart (time)
# 	xEnd (time)
# 	equipmentId
def ajaxPlot(request):
	if request.method == 'GET':
		try:
			goal = request.GET.get("goal", False)
			timeRange = request.GET.get("timeRange", "daily")
			timeFormat = Consumption.DATE_FORMAT_BR[timeRange]
			unit = request.GET.get("measurement", "kw")
			dateTimeStart = request.GET.get("xStart", datetime.now().strftime(timeFormat))
			dateTimeEnd = request.GET.get("xEnd", (datetime.strptime(dateTimeStart, timeFormat) + timedelta(days=-30)).strftime(timeFormat))
			# dateTimeStart = "01-09-2014"
			# dateTimeEnd = "01-10-2014"
			equipmentId = request.GET.getlist("equipmentId[]", None)
			income_type = request.user.profile.income_type
			integrate = request.GET.get("integrate", False)

			return_json = formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, unit, equipmentId, income_type, goal, integrate)

			return HttpResponse(json.dumps({'plots': return_json}), content_type="application/json")
		except Exception as e:
			print unicode(e.message)
			return HttpResponse(json.dumps({'plots': [[[]]]}), content_type="application/json")

def dateFormat(timeRange):
	if timeRange == "hourly":
		return "%Y-%m-%d %H:%M"
	elif timeRange == "daily":
		return "%Y-%m-%d"
	elif timeRange == "monthly":
		return "%Y-%m"

def formatToMoney(plotData, unit, start, end, mult, income_type, dateFormat):
	if unit == "money":
		# último aes antes da primeira data escolhida
		first_aes = AESRate.objects.filter(valid_date__lte=start, name=income_type).order_by("-valid_date").first()

		if first_aes:
			date1 = first_aes.valid_date
		else:
			date1 = start
		date2 = end
		rates = AESRate.objects.filter(valid_date__gte=date1, valid_date__lte=date2, name=income_type).order_by("-valid_date").values("range_start", "range_end", "te", "tusd", "valid_date")

		for index, item in enumerate(plotData):
			date_found = False

			for rate in rates:

				if rate["valid_date"] <= datetime.strptime(plotData[index][0], dateFormat).date() and not date_found:
					date_found = True

					# comparando os valores -> passando para kw
					if rate["range_start"]:
						if plotData[index][1]*0.001 < rate["range_start"]:
							date_found = False
							
					if rate["range_end"]:
						if plotData[index][1]*0.001 > rate["range_end"]:
							date_found = False

					# se não mudou, não achou data
					if date_found:
						# ele está em w -> passando para kw
						plotData[index][1] = plotData[index][1] * float(rate["tusd"] + rate["te"]) * 0.001

	else:
		for index, item in enumerate(plotData):
			plotData[index][1] = plotData[index][1] * mult

def formatIntegrate(plotData, integrate, timeRange, timeFormat):
	plotData = sorted(plotData, key=lambda x: x[0])
	if integrate:
		if integrate == True or integrate in ["true", "True"]:
			if timeRange == "hourly":
				sum = 0
				for index in range(len(plotData)):
					if index == 0:
						sum = plotData[0][1]
					else:
						sum = sum + plotData[index][1]
						plotData[index][1] = sum
			elif timeRange == "daily":
				sum = 0
				for index in range(len(plotData)):
					if index == 0:
						sum = plotData[0][1] * 24
					else:
						sum = sum + plotData[index][1] * 24
						plotData[index][1] = sum
			elif timeRange == "monthly":
				sum = 0
				for index in range(len(plotData)):
					timeDate = datetime.strptime(plotData[index][0], timeFormat)
					if index == 0:
						sum = plotData[0][1] * 24 * get_last_day_of_month(timeDate)
					else:
						sum = sum + plotData[index][1] * 24 * get_last_day_of_month(timeDate)
						plotData[index][1] = sum

def getConsumptionData(timeRange, equipmentId, unit, start, end, mult, integrate, income_type):
	return_json = None
	qs = Consumption.objects

	if equipmentId:
		
		if not ("" in equipmentId):
			ids = list(equipmentId)
			if "" in ids: ids.remove("")
			qs = qs.filter(equipment_id__in = ids)


	if timeRange == "hourly":
		qs = qs.values('moment', 'current', 'voltage', 'equipment_id').filter(moment__range=[start, end])

		return_json = map(lambda set: 
			[set['moment'].strftime(dateFormat(timeRange)), set['voltage'] * set['current'], set['equipment_id']], 
				qs
		)

	elif timeRange == "daily":
		end = end + timedelta(days=1)
		qs = qs.filter(moment__gte=start, moment__lt=end).extra({'moment': "date(moment)"}).values('moment', 'equipment_id').annotate(current=Avg('current'), voltage=Avg('voltage'))

		return_json = map(lambda set: 
			[set['moment'].strftime(dateFormat(timeRange)), set['voltage'] * set['current'], set['equipment_id']], 
				qs
		)

	elif timeRange == "monthly":
		end = get_last_day_of_month(end)
		qs = qs.filter(moment__gte=start, moment__lte=end)
		qs = qs.extra(select={'month': "EXTRACT(month FROM moment)", 'year': "EXTRACT(year FROM moment)"}).values('month')
		qs = qs.annotate(current_avg=Avg('current'), voltage_avg=Avg('voltage')).values('equipment_id', 'month', 'year', 'current_avg', 'voltage_avg')

		return_json = map(lambda set: 
			[datetime(int(set['year']), int(set['month']), 1).strftime(dateFormat(timeRange)), set['voltage_avg'] * set['current_avg'], set['equipment_id']], 
				qs
		)

	formatToMoney(return_json, unit, start, end, mult, income_type, dateFormat(timeRange))

	momentIndex = 0
	powerIndex = 1
	equipmentIdIndex = 2

	plotDatas = []

	# Foi pedido o grafico do somatorio
	plot = []

	if '' in equipmentId:
		groups = {}
		for obj in return_json:
			if not (obj[momentIndex] in groups):
				groups[obj[momentIndex]] = []

			groups[obj[momentIndex]].append( obj[powerIndex] )

		for moment in groups:
			sum = 0
			for value in groups[moment]:
				sum += value
			plot.append([moment, sum])

		plotDatas.append(plot)

	# Separando por id 
	for id in equipmentId:
		if id != "":
			plot = filter(lambda x: x[equipmentIdIndex] == int(id), return_json)
			if plot != None and len(plot) > 0:
				plotDatas.append(plot)

	return_json = plotDatas

	# formatToMoney(return_json, unit, start, end, mult, incomeType)

	for plotIndex in range(len(return_json)):
		formatIntegrate(return_json[plotIndex], integrate, timeRange, dateFormat(timeRange))

	return return_json

def getGoalData(equipmentId, consumptionData, dateFormat, start, end):

	goalLists= []

	qs = Goal.objects
	ids = list(equipmentId)
	if "" in ids: ids.remove("")
	if ids and len(ids) > 0:
		qs.filter(equipment=Equipment.objects.filter(pk__in = ids))

	goals = qs.filter(yearmonth_start__gte = start, yearmonth_end__lte = end) | \
					qs.filter(yearmonth_start__lte = start, yearmonth_start__gte = start) | \
					qs.filter(yearmonth_start__lte = end, yearmonth_start__gte = end)

	for plot in consumptionData:
		goalList = []
		for point in plot:
			newPoint = [point[0], 0]
			pointDate = datetime.strptime(point[0], dateFormat)

			for goal in goals:
				if goal.yearmonth_start <= pointDate.date():
					if goal.yearmonth_end <= pointDate.date():
						newPoint[1] = goal.value_absolute

			goalList.append(newPoint)

		if goalList != None and len(goalList) > 0:
			goalLists.append(goalList)

	return goalLists


def formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, unit, equipmentId, income_type, goal, integrate):
	aggregatedQuery= None
	# 0.001 para kW
	mult = 0.001 if unit == Equipment.MEASUREMENT_UNITS[1][0] else 1
	timeFormat = Consumption.DATE_FORMAT_BR[timeRange]
	start = datetime.strptime(dateTimeStart,timeFormat)
	end = datetime.strptime(dateTimeEnd,timeFormat)

	returnPlots = []

	consumptionData = getConsumptionData(timeRange, equipmentId, unit, start, end, mult, integrate, income_type)

	if goal ==  "true":
		goalData = getGoalData(equipmentId, consumptionData, dateFormat(timeRange), start, end)
		if goalData != None and len(goalData) > 0:
			consumptionData += goalData

	# Retornando os dados indexados para fazer a legenda
	indexedData = {}
	
	for i in range(len(equipmentId)):
		if equipmentId[i] == "":
			indexedData["all"] = consumptionData[i]
		else:
			indexedData[Equipment.objects.filter(pk = equipmentId[i])[0].name] = consumptionData[i]

	if goal in ["true", "True", True]:
		indexedData["goal"] = consumptionData[len(consumptionData) - 1]

	return indexedData
