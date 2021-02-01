from datetime import date 
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Company(models.Model):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, default='company_logos/cmp.png')
    address = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        img = Image.open(self.logo.path)

        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.logo.path)
    
    def get_absolute_url(self):
        return reverse('company-list')

class MyApplication(models.Model):
    
    class ApplicationType(models.TextChoices):
        INDEPENDENT = 'INDEP', _('Independent')
        ASSOCIATED = 'ASSOC', _('Associated')
    
    application_type = models.CharField(max_length=5,choices=ApplicationType.choices, default=ApplicationType.INDEPENDENT)
    applied_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    applied_to = models.ForeignKey(Company, on_delete=models.CASCADE, default='Select a company name', null=True)
    position = models.CharField(max_length=128, null=True, blank=True, default = None)
    attachment = models.FileField(blank=True, upload_to='cv_uploads/')
    comments = models.CharField(max_length=255, blank=True)
    cover_letter = models.TextField(blank=True)
    application_response = models.BooleanField(default=False)
    response_content = models.TextField(blank=True)

    def __str__(self):
        return f'{self.position} for {self.applied_to}'

    def get_absolute_url(self):    
        return reverse('landing-page')##, args=[str(self.id)])

class ApplicationTag(models.Model):
    name = models.CharField(verbose_name='Tags', max_length = 150, db_index=True, unique=True)
    applications = models.ManyToManyField(MyApplication, related_name="tags")

    def __str__(self):
        return self.name

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





