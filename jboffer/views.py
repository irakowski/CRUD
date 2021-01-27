from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from . import models
# Create your views here.

##HTML Rendering

class LandingPage(generic.TemplateView):
    '''
    Landing page of the website
    '''
    template_name = 'jboffer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all().order_by('-id')[:5]
        return context


class ApplicationView(generic.TemplateView):
    ...

class CreateApplication(generic.CreateView):
    
    model = models.MyApplication
    template_name = 'jboffer/forms/application_create_form.html'
    fields = ['application_type', 'applied_to', 'attachment', 'comments', 'cover_letter' ]
    

class UpdateApplication(generic.TemplateView):
    ...

class DeleteApplication(generic.TemplateView):
    ...



class CreateCompany(generic.CreateView):
    """
    Create Company db record upon successful form submittion
    Redirect to absolute url('/companies') upon success, 
    render form for re-submittion otherwise
    """
    model = models.Company
    template_name = 'jboffer/forms/company_create_form.html'
    fields = '__all__'


class CompanyListView(generic.ListView):
    """
    Render list of company records with latest created record at the top, 
    paginated by 4 items per page
    """
    context_object_name = 'companies'
    model = models.Company
    template_name = 'jboffer/lists/company_list.html'
    paginate_by = 4
    ordering = ['-id']

