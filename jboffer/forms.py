from django import forms
from . import models


class TagForm(forms.ModelForm):
   class Meta:
       model = models.ApplicationTag
       fields = ['name']
       widgets = {
          'name': forms.TextInput(attrs=
                {'placeholder':'#python #backend'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.MyApplication
        fields = ['application_type', 'applied_to', 'position', 'attachment', 'comments', 'cover_letter']


class ApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = models.MyApplication
        fields = ['comments', 'application_response', 'response_content']
        widgets = {
          'response_content': forms.Textarea(attrs={'rows':4, 'cols':25}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = models.JobOffer
        fields = ['description', 'snapshot', 'url']
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':25}),
        }