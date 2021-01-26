from datetime import date 
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    name = models.CharField(max_length=150)
    company_url = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse('company-details', kwargs={'pk': self.pk})

class MyApplication(models.Model):
    
    class ApplicationType(models.TextChoices):
        INDEPENDENT = 'INDEP', _('Independent')
        ASSOCIATED = 'ASSOC', _('Associated')
    
    application_type = models.CharField(max_length=5,choices=ApplicationType.choices)
    applied_to = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    applied_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(default=date.today)
    attachment = models.FileField(blank=True, upload_to='cv_uploads/')
    comments = models.TextField(blank=True)
    cover_letter = models.TextField(blank=True)
    application_response = models.BooleanField(default=False)
    response_content = models.TextField(blank=True)

    def __str__(self):
        return f'{self.position} for {self.applied_to}({self.applied_on})'

    def get_absolute_url(self):    
        return reverse('application', args=[str(self.id)])

    
class JobOffer(models.Model):
    short_description = models.CharField(max_length=255)
    offer_pic = models.ImageField(upload_to='scrshots/', blank=True)
    offer_url = models.CharField(max_length=255, )
    contact_email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=80, blank=True)
    position = models.CharField(max_length=100)
    application = models.ForeignKey(MyApplication, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.description} {self.offer_url}'





