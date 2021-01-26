from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from . import models
# Create your views here.

##HTML Rendering

class LandingPage(generic.TemplateView):
    '''
    Landing page of the website
    '''
    template_name = 'jboffer/base.html'


class ApplicationView(generic.TemplateView):
    ...

class CreateApplication(generic.CreateView):
    
    model = models.MyApplication
    template_name = 'jboffer/forms/application_create_form.html'
    fields = '__all__'#['application_type', 'applied_to', 'attachment', ]
   
    

class UpdateApplication(generic.TemplateView):
    ...

class DeleteApplication(generic.TemplateView):
    ...

class CreateCompany(generic.CreateView):

    model = models.Company
    template_name = 'jboffer/forms/company_create_form.html'
    fields = '__all__'
    success_url = reverse('landing-page')


