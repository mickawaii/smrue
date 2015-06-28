from django import forms
from django.template import Context, loader

class DatePicker(forms.DateInput):
	def render(self, name, value, attrs=None):
		template = loader.get_template('datepicker.html')

		context = dict()

		if attrs:
			if 'id' in attrs.keys():
				context['id'] = attrs['id']
		
		context['name'] = name
		context['attrs'] = self.attrs

		if value:
			if type(value) == unicode:
				context['value'] = value
			else:
				context['value'] = value.strftime(self.format)
		else:
			context['value'] = None

		context = Context(context)
		return template.render(context)
