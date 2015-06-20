from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateView

# Create your views here.
# class CoreListView(ListView, HasSystemMenuMixin):
# 	def get_context_data(self, **kwargs):
# 		context = super(CoreListView, self).get_context_data(**kwargs)
# 		context['menu_navbar'] = self.menu
		
# 		return context

class GraphicView(TemplateView):
  template_name = "consumption/graphic.html"

  # def get_context_data(self, **kwargs):
  #   context = super(View, self).get_context_data(**kwargs)

  #   context['page_title'] = 'Consumo'