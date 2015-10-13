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
		user = self.request.user

		if hasattr(user, 'profile'):
			context["income_type"] = user.profile.income_type

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
			# timeRange = request.GET.get("timeRange", "daily")
			timeRange = "daily"
			unit = request.GET.get("measurement", "kw")
			timeFormat = Consumption.DATE_FORMAT_BR[timeRange]

			dateTimeStart = "01-09-2014"
			
			dateTimeEnd = "01-10-2014"

			unit = "money"

			# dateTimeStart = request.GET.get("xStart", datetime.now().strftime(timeFormat))
			# dateTimeEnd = request.GET.get("xEnd", (datetime.strptime(dateTimeStart, timeFormat) + timedelta(days=-30)).strftime(timeFormat))
			# unit = request.GET.get("unit", Equipment.MEASUREMENT_UNITS[0][0])

			income_type = request.user.profile.income_type
			return_json = formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, unit, income_type)

			return HttpResponse(json.dumps({'plots': [return_json]}), content_type="application/json")
		except Exception as e:
			print unicode(e.message)
			return HttpResponse(json.dumps({'plots': [[[]]]}), content_type="application/json")

# Parâmetros usados:
	# code: código do sensor
	# voltage: medida de voltagem
	# current: corrente medida
def create(request):
	try:
		if request.method == 'POST':
			sensor = None
			try:
				sensor = Sensor.objects.get(code=request.POST.get("code", ""))
			except Sensor.DoesNotExist:
				sensor = Sensor.objects.create(code=request.POST.get("code", ""), name="template" + unicode(datetime.now()))
				sensor.save()

			current = request.POST.get("current", -1.0);
			voltage = request.POST.get("voltage", -1.0);

			if current > 0:
				if voltage > 0:
					Consumption.new(datetime.now(), current, voltage, sensor.equipment.id).save()

			return HttpReponse(status=201)
		else	:
			return HttpReponse(status=404)
	except:
		return HttpReponse(status=500)

def formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, unit, income_type):
	aggregatedQuery= None
	return_json = None	
	# 0.001 para kW
	mult = 0.001 if unit == Equipment.MEASUREMENT_UNITS[1][0] else 1
	timeFormat = Consumption.DATE_FORMAT_BR[timeRange]
	start = datetime.strptime(dateTimeStart,timeFormat)
	end = datetime.strptime(dateTimeEnd,timeFormat)

	if timeRange == "hourly":
		aggregatedQuery = Consumption.objects.values('moment', 'current', 'voltage').filter(moment__range=[start, end])

		return_json = map(lambda set: 
			[set['moment'].strftime("%Y-%m-%d"), set['voltage'] * set['current']], 
				aggregatedQuery
		)

	elif timeRange == "daily":
		end = end + timedelta(days=1)
		aggregatedQuery = Consumption.objects.filter(moment__gte=start, moment__lt=end).extra({'moment': "date(moment)"}).values('moment').annotate(current=Avg('current'), voltage=Avg('voltage'))

		return_json = map(lambda set: 
			[set['moment'].strftime("%Y-%m-%d"), set['voltage'] * set['current']], 
				aggregatedQuery
		)
		
	elif timeRange == "monthly":
		end = get_last_day_of_month(end)
		qs = Consumption.objects.filter(moment__gte=start, moment__lte=end)
		aggregatedQuery = qs.extra(select={'month': "EXTRACT(month FROM moment)", 'year': "EXTRACT(year FROM moment)"}).values('month').annotate(current_avg=Avg('current'), voltage_avg=Avg('voltage')).values('month', 'year', 'current_avg', 'voltage_avg')

		return_json = map(lambda set: 
			[datetime(int(set['year']), int(set['month']), 1).strftime("%Y-%m-%d"), set['voltage_avg'] * set['current_avg']], 
				aggregatedQuery
		)

	if unit == "money":
		date1 = AESRate.objects.filter(valid_date__lte=start, name=income_type).order_by("-valid_date").first().valid_date
		date2 = end
		rates = AESRate.objects.filter(valid_date__gte=date1, valid_date__lt=date2, name=income_type).order_by("-valid_date").values("range_start", "range_end", "te", "tusd", "valid_date")

		for index, item in enumerate(return_json):
			date_found = False

			for rate in rates:

				if rate["valid_date"] <= datetime.strptime(return_json[index][0], "%Y-%m-%d").date() and not date_found:
					date_found = True

					# comparando os valores -> passando para kw
					if rate["range_start"]:
						if return_json[index][1]*0.001 < rate["range_start"]:
							date_found = False
							
					if rate["range_end"]:
						if return_json[index][1]*0.001 > rate["range_end"]:
							date_found = False

					if date_found:
						return_json[index][1] = return_json[index][1] * float(rate["tusd"] + rate["te"]) * mult

	else:
		return_json = map(lambda moment, consumption: 
			[moment, consumption * mult], 
				return_json
		)


	print return_json

	return return_json