from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateView
from consumption.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from equipment.models import Equipment
from consumption.models import Consumption

from django.template import RequestContext
import unicodecsv

# Create your views here.
# class CoreListView(ListView, HasSystemMenuMixin):
# 	def get_context_data(self, **kwargs):
# 		context = super(CoreListView, self).get_context_data(**kwargs)
# 		context['menu_navbar'] = self.menu
		
# 		return context


# class GraphicView(TemplateView):
# 	form_class = UploadFileForm
# 	template_name = "consumption/graphic.html"
# 	form = UploadFileForm()

def graphicView(request):
	if request.method == 'POST': # If the form has been submitted...
		form = UploadFileForm(request.POST) # A form bound to the POST data
		# if form.is_valid(): # All validation rules pass
		csv_imported = request.FILES['csv']
		csv_imported.open()
		try:
			csv_reader = unicodecsv.DictReader(csv_imported, lineterminator = '\n', delimiter=';', encoding='latin-1')
			for line in csv_reader:
				Consumption.new(line['moment'], line['current'], line['voltage'], line['equipment_id']).save()
			return render_to_response('consumption/graphic.html', {'form': form}, context_instance=RequestContext(request))
		except Exception, e:
			return render_to_response('consumption/graphic.html', {'csv_error': 'Erro na leitura do csv'}, context_instance=RequestContext(request))