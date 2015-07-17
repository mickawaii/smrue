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

from django.template import RequestContext
from datetime import datetime, timedelta
import unicodecsv
import csv
import json
from django.db import connection
import calendar

class GraphicView(TemplateView):
	# form_class = UploadFileForm
	template_name = "consumption/graphic.html"
	# form = UploadFileForm()

	def get_context_data(self, **kwargs):
		context = super(GraphicView, self).get_context_data(**kwargs)

		context["measurement_units"] = Equipment.MEASUREMENT_UNITS
		context["months"] = ((1, "Janeiro"),(2, "Fevereiro"),(3, "Março"),(4, "Abril"),(5, "Maio"),(6, "Junho"),(7, "Julho"),(8, "Agosto"),(9, "Setembro"),(10, "Outubro"),(11, "Novembro"),(12, "Dezembro"))
		return context

def importCSV(request):
	if request.method == 'POST': # If the form has been submitted...
		# form = UploadFileForm(request.POST) # A form bound to the POST data
		# if form.is_valid(): # All validation rules pass
		csv_imported = request.FILES['csv']
		csv_imported.open()
		lineNumber = 0
		try:
			csv_reader = unicodecsv.DictReader(csv_imported, lineterminator = '\n', delimiter=';', encoding='UTF-8')
			for line in csv_reader:
				lineNumber += 1
				Consumption.new(line['moment'], line['current'], line['voltage'], line['equipment_id']).save()
			url = reverse('consumption:graphic')
			return HttpResponseRedirect(url)
		except Exception, e:
			url = reverse('consumption:graphic')
			messages.error(request, 'Erro na linha ' + str(lineNumber) + ' do CSV')
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

def formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, dateTimeFormat, magnitude):

	def get_first_day(dt, d_years=0, d_months=0):
		# d_years, d_months are "deltas" to apply to dt
		y, m = dt.year + d_years, dt.month + d_months
		a, m = divmod(m-1, 12)
		return datetime(y+a, m+1, 1)

	def get_last_day(dt):
		return get_first_day(dt, 0, 1) + timedelta(-1)

	aggregatedQuery= None
	dateFormat = ""
	return_json = None	
	import pdb; pdb.set_trace()

	if timeRange == "daily":
		aggregatedQuery = Consumption.objects.filter(moment__gte=datetime.strptime(dateTimeStart,dateTimeFormat), moment__lte=datetime.strptime(dateTimeEnd, dateTimeFormat) + timedelta(hours=23, minutes=59, seconds=59)).extra({'moment': "date(moment)"}).values('moment').annotate(current=Avg('current'), voltage=Avg('voltage'))
		dateFormat = "%Y-%m-%d"

		return_json = map(lambda set: 
			[set['moment'], set['voltage'] * set['current']], 
				aggregatedQuery
		)
		
	elif timeRange == "hourly":
		aggregatedQuery = Consumption.objects.values('moment', 'current', 'voltage').filter(moment__range=[datetime.strptime(dateTimeStart, dateTimeFormat), datetime.strptime(dateTimeEnd, dateTimeFormat)])
		dateFormat = "%Y-%m-%d %H:%M"

		return_json = map(lambda set: 
			[set['moment'].strftime(dateFormat), set['voltage'] * set['current']], 
				aggregatedQuery
		)

	elif timeRange == "monthly":
	
		truncate_date = connection.ops.date_trunc_sql('month', 'moment')
		qs = Consumption.objects.extra({'moment':truncate_date})

		aggregatedQuery = qs.filter(moment__gte=datetime.strptime(dateTimeStart,dateTimeFormat), moment__lte=get_last_day(datetime.strptime(dateTimeEnd, dateTimeFormat))).values('moment', 'current', 'voltage').annotate(current=Avg('current'), voltage=Avg('voltage'))
		dateFormat = "%Y-%m"

		return_json = map(lambda set: 
			[set['moment'], set['voltage'] * set['current']], 
				aggregatedQuery
		)
	
	return return_json

def ajaxPlot(request):
	if request.method == 'GET':
		try:
			import pdb; pdb.set_trace()

			timeFormat = ""
			timeRange = request.GET.get("timeRange", "daily")
			if timeRange == "daily":
				timeFormat = "%d-%m-%Y"
			elif timeRange == "hourly":
				timeFormat = "%d-%m-%Y %H:%M"
			elif timeRange == "monthly":
				timeFormat = "%m-%Y"


			print(timeFormat)

			dateTimeStart = request.GET.get("xStart", datetime.now().strftime(timeFormat))
			dateTimeEnd = request.GET.get("xEnd", (datetime.strptime(dateTimeStart, timeFormat) + timedelta(days=-30)).strftime(timeFormat))
			print(dateTimeEnd)
			unit = request.GET.get("unit", Equipment.MEASUREMENT_UNITS[0][0])

			magnitude = 1
			if unit == Equipment.MEASUREMENT_UNITS[0][0] or unit == Equipment.MEASUREMENT_UNITS[0][1]:
				magnitude = 1
			else:
				magnitude = 0.001
						
			print("HHHHHHHHHHHHHHHHHHHHHH")
			print(datetime.strptime(dateTimeStart, timeFormat))
			print(datetime.strptime(dateTimeEnd, timeFormat))
			
			return_json = formatDataToPlotData(timeRange, dateTimeStart, dateTimeEnd, timeFormat, magnitude)

			print(return_json)
			return HttpResponse(json.dumps({'plots': [[return_json]]}), content_type="application/json")
		except:
			return HttpResponse(json.dumps({'plots': [[[]]]}), content_type="application/json")
