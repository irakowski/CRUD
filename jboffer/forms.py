from django import forms
from . import models


class TagForm(forms.ModelForm):
   class Meta:
       model = models.ApplicationTag
       fields = ['name']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.MyApplication
        fields = ['application_type', 'applied_to', 'position', 'attachment', 'comments', 'cover_letter']
