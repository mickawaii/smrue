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
from django.db import connection
import calendar
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from exceptions import ValueError

class GraphicView(TemplateView):
	# form_class = UploadFileForm
	template_name = "consumption/graphic.html"
	# form = UploadFileForm()

	def get_context_data(self, **kwargs):
		context = super(GraphicView, self).get_context_data(**kwargs)

		context["measurement_units"] = Equipment.MEASUREMENT_UNITS
		context["months"] = ((1, "Janeiro"),(2, "Fevereiro"),(3, "Março"),(4, "Abril"),(5, "Maio"),(6, "Junho"),(7, "Julho"),(8, "Agosto"),(9, "Setembro"),(10, "Outubro"),(11, "Novembro"),(12, "Dezembro"))
		return context

def get_first_day_of_month(dt, d_years=0, d_months=0):
	# d_years, d_months are "deltas" to apply to dt
	y, m = dt.year + d_years, dt.month + d_months
	a, m = divmod(m-1, 12)
	return datetime(y+a, m+1, 1)

def get_last_day_of_month(dt):
	return get_first_day_of_month(dt, 0, 1) + timedelta(-1)

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
			import pdb; pdb.set_trace()
			messages.error(request, "Linha "  + str(lineNumber) + ": " + str(e3))
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

def ajaxPlot(request):
	if request.method == 'GET':
		try:
			goal = request.GET.get("goal", True)
			timeFormat = ""
			# timeRange = request.GET.get("timeRange", "daily")
			moneyFormat = request.GET.get("money", True)

			timeRange = "daily"



			if timeRange == "daily":
				timeFormat = "%d-%m-%Y"
			elif timeRange == "hourly":
				timeFormat = "%d-%m-%Y %H:%M"
			elif timeRange == "monthly":
				timeFormat = "%m-%Y"


			dateTimeStart = "01-09-2014"
			
			dateTimeEnd = "01-10-2014"

			unit = "kw"

			# dateTimeStart = request.GET.get("xStart", datetime.now().strftime(timeFormat))
			# dateTimeEnd = request.GET.get("xEnd", (datetime.strptime(dateTimeStart, timeFormat) + timedelta(days=-30)).strftime(timeFormat))
			# unit = request.GET.get("unit", Equipment.MEASUREMENT_UNITS[0][0])
			goal = []

			return_json = formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, timeFormat, unit)

			# if moneyFormat:
			# 	income_type = request.user.profile.income_type
			# 	return_json = formatToMoneyData(timeRange, dateTimeStart, dateTimeEnd, timeFormat, unit, income_type, return_json)


			return HttpResponse(json.dumps({'plots': [[return_json]]}), content_type="application/json")
		except Exception as e:
			print unicode(e.message)
			return HttpResponse(json.dumps({'plots': [[[]]]}), content_type="application/json")

# Parâmetros usados:
	# code: código do sensor
	# voltage: medida de voltagem
	# current: corrente medida
def create(request):
	try:
		# import pdb; pdb.set_trace()
		if request.method == 'POST':
			code = request.POST.get("code", "").encode("utf-8")
			print(code)
			current = request.POST.get("current", -1.0);
			voltage = request.POST.get("voltage", -1.0);

			

			sensor = None
			try:
				sensor = Sensor.objects.get(code=code)
			except Sensor.DoesNotExist:
				sensor = Sensor.objects.create(code=code, name="template" + unicode(datetime.now()))
				sensor.save()

			if current > 0:
				if voltage > 0:
					Consumption.new(datetime.now(), current, voltage, sensor.equipment.id).save()

			return HttpResponse(status=201)
		else	:
			return HttpResponse(status=404)
	except Exception as e:
		print(error)
		return HttpResponse(status=500)

def formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, dateTimeFormat, unit):
	aggregatedQuery= None
	dateFormat = ""
	return_json = None	
	mult = 0.001 if unit == Equipment.MEASUREMENT_UNITS[1][0] else 1

	if timeRange == "daily":
		aggregatedQuery = Consumption.objects.filter(moment__gte=datetime.strptime(dateTimeStart,dateTimeFormat), moment__lt=datetime.strptime(dateTimeEnd, dateTimeFormat) + timedelta(days=1)).extra({'moment': "date(moment)"}).values('moment').annotate(current=Avg('current'), voltage=Avg('voltage'))
		dateFormat = "%Y-%m-%d"

		return_json = map(lambda set: 
			[set['moment'].strftime(dateFormat), mult * set['voltage'] * set['current']], 
				aggregatedQuery
		)
		
	elif timeRange == "hourly":
		aggregatedQuery = Consumption.objects.values('moment', 'current', 'voltage').filter(moment__range=[datetime.strptime(dateTimeStart, dateTimeFormat), datetime.strptime(dateTimeEnd, dateTimeFormat)])
		dateFormat = "%Y-%m-%d %H:%M"

		return_json = map(lambda set: 
			[set['moment'].strftime(dateFormat), mult * set['voltage'] * set['current']], 
				aggregatedQuery
		)

	elif timeRange == "monthly":
		# import pdb; pdb.set_trace()
		# truncate_date = connection.ops.date_trunc_sql('month', 'moment')
		qs = Consumption.objects.filter(moment__gte=datetime.strptime(dateTimeStart,dateTimeFormat), moment__lte=get_last_day_of_month(datetime.strptime(dateTimeEnd, dateTimeFormat)))
		aggregatedQuery = qs.extra(select={'month': "EXTRACT(month FROM moment)", 'year': "EXTRACT(year FROM moment)"}).values('month').annotate(current_avg=Avg('current'), voltage_avg=Avg('voltage')).values('month', 'year', 'current_avg', 'voltage_avg')
		dateFormat = "%Y-%m"

		return_json = map(lambda set: 
			[datetime(int(set['year']), int(set['month']), 1).strftime(dateFormat), mult * set['voltage_avg'] * set['current_avg']], 
				aggregatedQuery
		)

	return return_json

def formatToMoneyData(timeRange, dateTimeStart, dateTimeEnd, timeFormat, unit, incomeType, jsonData):
	# se dinheiro
	# monta intervalo

	if timeRange == "hourly":
		dateStartFilter = datetime.strptime(dateTimeStart, timeFormat)
		dateEndFilter = datetime.strptime(dateTimeEnd, timeFormat)

	elif timeRange == "daily":
		dateStartFilter = datetime.strptime(dateTimeStart, timeFormat)
		dateEndFilter = datetime.strptime(dateTimeEnd, timeFormat)+timedelta(days=1)

	elif timeRange == "monthly":
		dateStartFilter = datetime.strptime(dateTimeStart, timeFormat)
		dateEndFilter = get_last_day_of_month(datetime.strptime(dateTimeEnd, timeFormat))

	date1 = AESRate.objects.filter(valid_date__lte=dateStartFilter, name=incomeType).order_by("-valid_date").first().valid_date
	date2 = dateEndFilter
	rates = AESRate.objects.filter(valid_date__gte=date1, valid_date__lt=date2, name=incomeType).order_by("-valid_date").values("range_start", "range_end", "te", "tusd", "valid_date")

	for i in xrange(len(jsonData)-1):
		date_found = False

		for rate in rates:

			if rate["valid_date"] <= datetime.strptime(jsonData[i][0], "%Y-%m-%d").date() and not date_found:
				if unit == Equipment.MEASUREMENT_UNITS[0][0] or unit == Equipment.MEASUREMENT_UNITS[0][1]:
					unit = 1
				else:
					unit = 0.001















				jsonData[i][1] = jsonData[i][1] * float(rate["tusd"] + rate["te"]) * 1000
				date_found = True

	return jsonData
