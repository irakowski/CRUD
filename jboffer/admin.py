from django.contrib import admin
from jboffer.models import Company, ApplicationTag, MyApplication, JobOffer

admin.site.register(Company)
admin.site.register(ApplicationTag)
admin.site.register(MyApplication)
admin.site.register(JobOffer)

# Register your models here.
