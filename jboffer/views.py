import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from . import models
from . import forms


class LandingPage(generic.TemplateView):
    '''
    Landing page of the website. Queries five latest company and offer records 
    and three application records for display in the template
    '''
    template_name = 'jboffer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = models.Company.objects.order_by('-id')[:5]
        context['apps'] = models.MyApplication.objects.order_by('-id')[:3]
        context['offers'] = models.JobOffer.objects.order_by('-id')[:5]
        return context


def ajax_update(request, pk):
    """
    Handles AJAX call for application update
    """
    if request.method == "POST" and request.is_ajax():
        app = get_object_or_404(models.MyApplication, pk=pk)
        form = forms.ApplicationUpdateForm(request.POST, instance=app)           
        if form.is_valid():
            instance = form.save()
            app =list(models.MyApplication.objects.filter(pk=instance.pk).values())
            #Might as well return HttpReponse
            return JsonResponse({"status": "success", "app": app}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


def ajax_delete(request, pk):
    """
    Handles AJAX call for application delete
    """
    if request.method == "POST" and request.is_ajax():
        app = models.MyApplication.objects.get(pk=pk)
        app.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"error": form.errors}, status=400)


class CreateApplication(generic.TemplateView):
    """
    View rendering ModelForm for application create. 
    Renders two additional forms: 
        - Form for creating and/or associating tags with given application
        - Form for creating and associating job offers with given application
          (applicable to applications of application_type 'ASSOC')
    """
    template_name = 'jboffer/forms/application_create_form.html'
    success_url = reverse_lazy('landing-page')

    def get_context_data(self, **kwargs):
        """
        Adding all forms for display on GET
        """
        if 'form' not in kwargs and 'tag_form' not in kwargs and 'offer_form' not in kwargs:
            kwargs['form'] = forms.ApplicationForm()
            kwargs['tag_form'] = forms.TagForm()
            kwargs['offer_form'] = forms.OfferForm()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate three form instances: 
        - Form for creating Application  
        - Form for creating tags
        - Form for creating JobOffer(only if app_type == "ASSOC")
        Saves application instance along with associated tags and 
        Joboffer instance if applicable
        """
        form = forms.ApplicationForm(self.request.POST, self.request.FILES)
        tag_form = forms.TagForm(self.request.POST)
        #ApplicationForm and TagForm must be valid first
        if form.is_valid() and tag_form.is_valid():
            #get value of selected application_type
            app_type = form.cleaned_data.get('application_type')
            if app_type == 'ASSOC':
                #get JobOffer Form with passed values
                offer_form = forms.OfferForm(self.request.POST, self.request.FILES)
                if offer_form.is_valid():
                    return self.form_valid(form, tag_form, offer_form)
                #return same view if form is invalid
                return self.form_invalid(form, tag_form, offer_form)
            #sending valid ApplicationForm and TagForm to form_valid method for saving instances
            return self.form_valid(form, tag_form, offer_form=None)
        else:
            return self.form_invalid(form, tag_form, offer_form=None)

    def form_valid(self, form, tag_form, offer_form):
        """If the form is valid, redirect to the supplied URL."""
        application = form.save()
        tags = tag_form.cleaned_data.get('name')
        tags = tags.split()
        
        for tag in tags:
            if tag.lower().startswith('#'):
                tag = tag.lower()[1:]
            else:
                tag = tag.lower()
            #Checking if such tag exists in db
            if models.ApplicationTag.objects.filter(name=tag).exists():
                ##adding application to the avai1lable tag
                application.tags.add(models.ApplicationTag.objects.get(name=tag))
            else:
                #creating new tag
                application.tags.create(name=tag)
        application.save()
        if offer_form:
            offer = offer_form.save()
            offer.application = application
            offer.save()
            return HttpResponseRedirect(self.success_url)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, tag_form, offer_form):
        return self.render_to_response(self.get_context_data(form=form, tag_form=tag_form, offer_form=offer_form))


class ApplicationsByTag(generic.View):
    """ 
    Filter applications based on selected tag
    Render list of application associated with given tag, 
    paginated by 3 items per page
    """
    paginate_by = 3

    def get(self, request, tag):
        apps_list = models.MyApplication.objects.filter(tags__name=tag)
        paginator = Paginator(apps_list, self.paginate_by) # Show 4 apps per page.
    
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        try:
            apps = paginator.page(page_number)
        except PageNotAnInteger:
            apps = paginator.page(1)
        except EmptyPage:
            apps = paginator.page(paginator.num_pages)
            
        context = {
            'tag': tag,
            'apps': apps,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1, 
        }

        return render(self.request, 'jboffer/lists/apps_by_tag.html', context)


class ViewApplication(generic.DetailView):
    """
    View displaying single application instance.
    Renders Form for updating application through Ajax call.
    """
    template_name = 'jboffer/view/application_view.html'
    model = models.MyApplication
    context_object_name = 'app'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ApplicationUpdateForm(instance=self.object)
        return context


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
    Render list of company records sorted by id descending 
    paginated by 4 items per page
    """
    context_object_name = 'companies'
    model = models.Company
    template_name = 'jboffer/lists/company_list.html'
    paginate_by = 4
    ordering = ['-id']


class JobOfferListView(generic.ListView):
    """
    Render list of job offers sorted by id descending, 
    paginated by 4 items per page
    """
    context_object_name = 'offers'
    model = models.JobOffer
    template_name = 'jboffer/lists/job_offer_list.html'
    paginate_by = 4
    ordering = ['-id']


class JobOfferDetailView(generic.DetailView):
    """
    Single job offer display
    """
    model = models.JobOffer
    template_name = 'jboffer/view/joboffer_view.html'
    context_object_name = 'offer'


class Stats(generic.TemplateView):
    """
    View for Database Records Statistic.
    Queries recent(15days) applications for display
    """    
    template_name = 'jboffer/stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_applications = models.MyApplication.objects.count()
        number_of_indep_apps = models.MyApplication.objects.filter(application_type="INDEP").count()
        context['total_applications'] = total_applications
        context['number_of_indep_apps'] = models.MyApplication.objects.filter(application_type="INDEP").count()
        context['number_of_assoc_apps'] = total_applications - number_of_indep_apps
        context['replies'] = models.MyApplication.objects.filter(application_response=True).count()
        context['companies'] = models.Company.objects.count()
        today = timezone.now()
        before = today - datetime.timedelta(days=15)
        context['apps'] = models.MyApplication.objects.filter(applied_on__range=[before, today])
        return context
