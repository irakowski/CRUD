"""ojom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from jboffer import views as general_views

urlpatterns = [
    path('', general_views.LandingPage.as_view(), name='landing-page'),     
    path('application/new', general_views.CreateApplication.as_view(), name='create-application'),
    path('application/<int:id>', general_views.ApplicationView.as_view(), name='application-display'),
    path('application/update/<int:id>', general_views.UpdateApplication.as_view(), name='update-application'),
    path('application/delete/<int:id>', general_views.DeleteApplication.as_view(), name='delete-application'),
    path('company/new', general_views.CreateCompany.as_view(), name='create-company'),
    path('companies/', general_views.CompanyListView.as_view(), name='company-list'),
    path('admin/', admin.site.urls),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
