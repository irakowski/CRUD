import json
import datetime
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from . import models
from . import forms


class LandingPage(generic.TemplateView):
    '''
    Landing page of the website
    '''
    template_name = 'jboffer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = models.Company.objects.order_by('-id')[:5]
        context['apps'] = models.MyApplication.objects.order_by('-id')[:3]
        context['offers'] = models.JobOffer.objects.order_by('-id')[:5]
        return context

def ajax_update(request, pk):
    if request.method == "POST"and request.is_ajax():
        app = models.MyApplication.objects.get(pk=pk)
        form = forms.ApplicationUpdateForm(request.POST, instance=app)           
        if form.is_valid():
            instance = form.save()
            app =list(models.MyApplication.objects.filter(pk=instance.pk).values())
            return JsonResponse({"status": "success", "app": app}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)

def ajax_delete(request, pk):
    if request.method == "POST" and request.is_ajax():
        app = models.MyApplication.objects.get(pk=pk)
        app.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"error": form.errors}, status=400)

class CreateApplication(generic.TemplateView):
    """
    Renders form to create record in application table and 
    create tag record in ApplicationTags table associated with given application
    """
    template_name = 'jboffer/forms/application_create_form.html'
    success_url = reverse_lazy('landing-page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ApplicationForm()
        context['tag_form'] = forms.TagForm()
        context['offer_form'] = forms.OfferForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate two form instances: 
        - Form for creating Application  
        - Form for creating tags
        - Form for creating JobOffer(only if app_type == "ASSOC")
        Saves application instance along with associated tags.
        """
        form = forms.ApplicationForm(self.request.POST, self.request.FILES)
        tag_form = forms.TagForm(self.request.POST)
        if form.is_valid() and tag_form.is_valid():
            app_type = form.cleaned_data.get('application_type')
            if app_type == 'ASSOC':
                offer_form = forms.OfferForm(self.request.POST, self.request.FILES)
                if offer_form.is_valid():
                    return self.form_valid(form, tag_form, offer_form)
                return self.form_invalid(form, tag_form, offer_form)
            return self.form_valid(form, tag_form, offer_form=None)
        else:
            return self.form_invalid(form, tag_form, offer_form)

    def form_valid(self, form, tag_form, offer_form):
        """If the form is valid, redirect to the supplied URL."""
        application = form.save()
        tags = tag_form.cleaned_data.get('name')
        tags = tags.split()
        ###Get the names of previously created tags
        prev_tags = list(models.ApplicationTag.objects.values_list('name', flat=True))
        for tag in tags:
            if tag.lower().startswith('#'):
                tag = tag.lower()[1:]
            else:
                tag = tag.lower()
            if tag in prev_tags:
                ##adding application to the available tag
                application.tags.add(models.ApplicationTag.objects.get(name=tag))
            else:
                #creating new tag
                application.tags.create(name=tag)
        application.save()
        if offer_form:
            print(offer_form)
            offer = offer_form.save()
            offer.application = application
            offer.save()
            return HttpResponseRedirect(self.success_url)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, tag_form, offer_form):
        return self.render_to_response(self.get_context_data())


class ApplicationsByTag(generic.View):
    """ 
    Filter applications based on selected tag
    Render list of application associated with given tag
    """        
    def get(self, request, tag):
        context = {}
        context['tag'] = tag
        context['apps'] = models.MyApplication.objects.filter(tags__name=tag)
        return render(self.request, 'jboffer/lists/apps_by_tag.html', context)


class ViewApplication(generic.DetailView):

    template_name = 'jboffer/forms/application_update_form.html'
    model = models.MyApplication
    context_object_name = 'app'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ApplicationUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        return ajax_update(self.request)
        
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

class JobOfferListView(generic.ListView):
    context_object_name = 'offers'
    model = models.JobOffer
    template_name = 'jboffer/lists/job_offer_list.html'
    paginate_by = 4
    ordering = ['-id']

class JobOfferDetailView(generic.DetailView):
    ...

class Stats(generic.TemplateView):
    template_name = 'jboffer/stats.html'
    
    def get_context_data(self):
        super().get_context_data()
        context = {}
        context['total_applications'] = models.MyApplication.objects.count()
        context['number_of_indep_apps'] = models.MyApplication.objects.filter(application_type="INDEP").count()
        context['number_of_assoc_apps'] = models.MyApplication.objects.filter(application_type="ASSOC").count()
        context['replies'] = models.MyApplication.objects.filter(application_response=True).count()
        context['companies'] = models.Company.objects.count()
        today = timezone.now()
        before = today - datetime.timedelta(days=30)
        context['apps'] = models.MyApplication.objects.filter(applied_on__range=[before, today])
        return context

