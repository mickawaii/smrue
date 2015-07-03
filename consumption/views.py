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

class GraphicView(TemplateView):
	# form_class = UploadFileForm
	template_name = "consumption/graphic.html"
	# form = UploadFileForm()

	def get_context_data(self, **kwargs):
		context = super(GraphicView, self).get_context_data(**kwargs)

		context["measurement_units"] = Equipment.MEASUREMENT_UNITS
		return context

def importCSV(request):
	if request.method == 'POST': # If the form has been submitted...
		# form = UploadFileForm(request.POST) # A form bound to the POST data
		# if form.is_valid(): # All validation rules pass
		csv_imported = request.FILES['csv']
		csv_imported.open()
		line = 0
		try:
			csv_reader = unicodecsv.DictReader(csv_imported, lineterminator = '\n', delimiter=';', encoding='latin-1')
			for line in csv_reader:
				line += 1
				Consumption.new(line['moment'], line['current'], line['voltage'], line['equipment_id']).save()
			url = reverse('consumption:graphic')
			return HttpResponseRedirect(url)
		except Exception, e:
			url = reverse('consumption:graphic')
			messages.error(request, 'Erro na linha %d do CSV', str(line))
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

def ajaxPlot(request):
	if request.method == 'GET':
		try:
			timeFormat = ""
			timeRange = request.GET.get("timeRange", "daily")

			if timeRange == "daily":
					timeFormat = "%d-%m-%Y"
			else:
				if timeRange == "hourly":
					timeFormat = "%d-%m-%Y %I:%M %p"

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
			
			return_json = map(lambda set: 
				[set['moment'].strftime("%Y-%m-%d %H:%M"), set['voltage'] * set['current'] * magnitude], 
				Consumption.objects.values('moment', 'current', 'voltage').filter(moment__range=[datetime.strptime(dateTimeStart, timeFormat), datetime.strptime(dateTimeEnd, timeFormat)])
			)
			return HttpResponse(json.dumps({'plots': [[return_json]]}), content_type="application/json")
		except:
			return HttpResponse(json.dumps({'plots': [[[]]]}), content_type="application/json")
