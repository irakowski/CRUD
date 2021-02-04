import pytest
from django.shortcuts import reverse
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
from jboffer.forms import ApplicationForm
from jboffer.models import ApplicationTag, MyApplication, Company, JobOffer

fake = Faker()


@pytest.mark.django_db
def test_landing_page(client):
    """
    GET Request on landing page with no data
    """
    response = client.get(reverse('landing-page'))
    assert not 'companies' in response.context
    assert response.status_code == 200


@pytest.mark.django_db
def test_landing_page(client, fake_companies):
    """
    GET Request on landing page with populated db
    """
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200
    assert 'companies' in response.context
    assert len(response.context['companies']) == 5


@pytest.mark.django_db
def test_create_application(client):
    """
    Simple GET request on create_application view, confirming 
    all forms are passed through context 
    """
    response = client.get(reverse('create-application'))
    assert response.status_code == 200
    assert 'tag_form' in response.context
    assert 'form' in response.context
    assert 'offer_form' in response.context

@pytest.mark.django_db
def test_create_application_post_success(client, fake_company):
    """
    Successfull form submition creates Application Instance 
    and tags associated with that instance
    """
    create_app_url = reverse('create-application')
    form_data =  {   
        'application_type': 'INDEP',
        'applied_to': fake_company.id,
        'position': 'Some random position', 
        'cover_letter': fake.paragraph(nb_sentences=3),
        'name': '#faketag #tests'
    }
    response = client.post(create_app_url, form_data)
    assert response.status_code == 302
    assert response.url == reverse('landing-page') 
    app = MyApplication.objects.get(position='Some random position')
    assert app.applied_to == fake_company
    assert app in MyApplication.objects.all()
    tag1 = ApplicationTag.objects.get(name='faketag')
    tag2 = ApplicationTag.objects.get(name='tests')
    assert tag1 and tag2 in app.tags.all()


@pytest.mark.django_db
def test_create_application_post_fail(client, fake_company):
    """
    Attemp to create an application without required field 
    redirects to same view with form errors in response.content
    """
    create_app_url = reverse('create-application')
    form_data =  {   
        'application_type': 'ASSOC',
        'applied_to': fake_company,
        #'position': 'Some random position', Skipping required field 
        'cover_letter': fake.paragraph(nb_sentences=5),
        'name': '#faketag #tests'
    }
    response = client.post(create_app_url, form_data)
    assert response.status_code == 200
    assert b'This field is required' in response.content


@pytest.mark.django_db
def test_tags_list(client):
    


@pytest.mark.django_db
def test_application_view_success(client, fake_applications):
    apps = MyApplication.objects.all()
    for app in apps:
        response = client.get(reverse('view-application', kwargs={'pk':app.id}))
        assert response.status_code == 200


@pytest.mark.django_db
def test_application_view_404(client, fake_applications):
    last_app = MyApplication.objects.last()
    response = client.get(reverse('view-application', kwargs={'pk':last_app.id+50}))
    assert response.status_code == 404
    assert b'Not Found' in response.content

@pytest.mark.django_db
def test_create_job_offer_post_success(client, fake_company):
    """
    Confirms creating Application with application_type set to 
    'ASSOC' will automatically create related Job Offer
    """
    create_offer_url = reverse('create-application')
    form_data =  {   
        'application_type': 'ASSOC',
        'applied_to': fake_company.id,
        'position': 'Position',
        'cover_letter': fake.paragraph(nb_sentences=5),
        'name': '#tag #tests'
    }
    response = client.post(create_offer_url, form_data)
    assert response.status_code == 302
    app = MyApplication.objects.get(position='Position')
    assert JobOffer.objects.filter(application=app).exists()


@pytest.mark.django_db
def test_create_company_success(client):
    temp_file = SimpleUploadedFile("file.png", 
            content=open('jboffer/tests/files/django.png', 'rb').read(), 
            content_type="image/png")

    create_company_url = reverse('create-company')
    form_data =  {   
        'name': 'FakeName LLC',
        'url': fake.url(),
        'email': fake.company_email(),
        'logo': temp_file
    }
    response = client.post(create_company_url, form_data)
    assert response.status_code == 302
    assert Company.objects.filter(name='FakeName LLC').exists()


@pytest.mark.django_db
def test_create_company_fail(client):
    temp_file = SimpleUploadedFile("file.png", 
            content=open('jboffer/tests/files/django.png', 'rb').read(), 
            content_type="image/png")

    create_company_url = reverse('create-company')
    form_data =  {   
        #'name': 'FakeName LLC', #SKIPPING REQUIRED FIELD
        'url': fake.url(),
        'email': 'fake_email@jboffer.com',
        'logo': temp_file
    }
    response = client.post(create_company_url, form_data)
    assert response.status_code == 200
    assert not Company.objects.filter(email='fake_email@jboffer.com').exists()
    assert b'This field is required' in response.content


@pytest.mark.django_db
def test_create_job_offer_post_fail(client, fake_company):
    """
    Confirms creating Application with Application_type set to 'INDEP'
    will not automatically create related Job offer instance
    """
    
    create_offer_url = reverse('create-application')
    form_data =  {   
        'application_type': 'INDEP',
        'applied_to': fake_company.id,
        'position': 'Some Position',
        'cover_letter': fake.paragraph(nb_sentences=5),
        'name': '#tag #tests'
    }
    response = client.post(create_offer_url, form_data)
    assert response.status_code == 302
    app = MyApplication.objects.get(position='Some Position')
    assert not JobOffer.objects.filter(application=app).exists()


@pytest.mark.django_db
def test_company_list_view(client, fake_companies):
    response = client.get(reverse('company-list'))
    companies = Company.objects.count()
    assert response.status_code == 200
    if companies > 4:
        assert response.context['is_paginated'] == True
        assert len(response.context['companies']) == 4
    else:
        assert response.context['is_paginated'] == False
        assert len(response.context['companies']) == Company.objects.count()
    assert 'companies' in response.context


@pytest.mark.django_db
def test_job_offer_list_view(client, fake_job_offers):
    response = client.get(reverse('job-offer-list'))
    job_offers = JobOffer.objects.count()
    assert response.status_code == 200
    assert 'offers' in response.context
    if job_offers > 4:
        assert response.context['is_paginated'] == True
        assert len(response.context['offers']) == 4
    else:
        assert response.context['is_paginated'] == False
        assert len(response.context['offers']) == JobOffer.objects.count()


@pytest.mark.django_db
def test_job_offer_detail_view(client, fake_job_offers):
    """
    Returns OK status on all job_offer records presented in the table
    """
    job_offers = JobOffer.objects.all()
    for offer in job_offers:
        offer_url = reverse('view-offer', kwargs={'pk': offer.id})
        response = client.get(offer_url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_job_offer_detail_view_404(client, fake_job_offers):
    """
    Page not found on view that doesnt match any job_offers in db
    """
    last = JobOffer.objects.last()
    job_offer_does_not_exist = last.id + 50
    response = client.get(reverse('view-offer', kwargs={'pk':job_offer_does_not_exist}))
    assert response.status_code == 404


from django.utils import timezone
import datetime
@pytest.mark.django_db
def test_stats_view(client, fake_company,fake_companies, fake_applications, fake_job_offers):
    """
    Statistics are displayed correctly in accordance with database records.
    Applications get filtered accordingly  
    """    
    today = timezone.now()
    created_25_days_ago = today - datetime.timedelta(days=25)
   
    app = MyApplication.objects.create(application_type='INDEP',
                                applied_to=fake_company,
                                position=fake.job())
    app.applied_on = created_25_days_ago
    app.save()
    response = client.get(reverse('stats'))

    assert response.status_code == 200
    assert 'total_applications' in response.context
    assert response.context['total_applications'] == MyApplication.objects.count()
    assert 'number_of_assoc_apps' in response.context 
    assert response.context['number_of_assoc_apps'] == MyApplication.objects.filter(application_type='ASSOC').count()
    assert app not in response.context['apps']
