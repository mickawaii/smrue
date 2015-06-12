from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.conf import settings

# Create your views here.
# class CoreListView(ListView, HasSystemMenuMixin):
# 	def get_context_data(self, **kwargs):
# 		context = super(CoreListView, self).get_context_data(**kwargs)
# 		context['menu_navbar'] = self.menu
		
# 		return context