from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template.context import Context

# Create your views here.
def send_email(subject, from_email, to_email, template_name, context={}):
	template = get_template(template_name+'.html')
	c = Context(context)

	html = template.render(c)

	print subject, from_email, to_email, template_name
	msg = EmailMessage(subject, html, from_email, to_email)
	msg.content_subtype = "html"
	msg.send()

	return 'email sent'