from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateView
from consumption.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from equipment.models import Equipment
from consumption.models import Consumption

from django.template import RequestContext
import unicodecsv
import csv
import json

# Create your views here.
# class CoreListView(ListView, HasSystemMenuMixin):
# 	def get_context_data(self, **kwargs):
# 		context = super(CoreListView, self).get_context_data(**kwargs)
# 		context['menu_navbar'] = self.menu
		
# 		return context


class GraphicView(TemplateView):
	form_class = UploadFileForm
	template_name = "consumption/graphic.html"
	form = UploadFileForm()

def importCSV(request):
	if request.method == 'POST': # If the form has been submitted...
		form = UploadFileForm(request.POST) # A form bound to the POST data
		# if form.is_valid(): # All validation rules pass
		csv_imported = request.FILES['csv']
		csv_imported.open()
		try:
			csv_reader = unicodecsv.DictReader(csv_imported, lineterminator = '\n', delimiter=';', encoding='latin-1')
			for line in csv_reader:
				Consumption.new(line['moment'], line['current'], line['voltage'], line['equipment_id']).save()
			url = reverse('consumption:graphic')
			return HttpResponseRedirect(url)
		except Exception, e:
			url = reverse('consumption:graphic')
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
		print(Consumption.objects.values('moment', 'current', 'voltage').all())
		return_json = map(lambda set: 
			[set['moment'].strftime("%d-%m-%Y"), set['voltage'] * set['current']], 
			Consumption.objects.values('moment', 'current', 'voltage').all())

		return HttpResponse(json.dumps({'plot': return_json}), content_type="application/json")

	return response