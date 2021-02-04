import random
import pytest
from faker import Faker
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from jboffer.models import MyApplication, Company, JobOffer, ApplicationTag

@pytest.fixture
def client():
    """
    Returns client used in tests
    """
    client = Client()
    return client


fake = Faker()
@pytest.fixture
def fake_company():
    """
    Creates Companies
    """
    temp_file = SimpleUploadedFile("file.png", 
            content=open('jboffer/tests/files/django.png', 'rb').read(), 
            content_type="image/png")
    company = Company(name=fake.company(),
                      url=fake.url(),
                      address = fake.address(),
                      email=fake.company_email(),
                      logo=temp_file)
    company.save()
    return company


@pytest.fixture
def fake_companies():
    """
    Creates Companies
    """
    temp_file = SimpleUploadedFile("file.png", 
            content=open('jboffer/tests/files/django.png', 'rb').read(), 
            content_type="image/png")
    for _ in range(9):
        company = Company(name=fake.company(),
                          url=fake.url(),
                          address = fake.address(),
                          email=fake.company_email(),
                          logo=temp_file)
        company.save()
    return company


@pytest.fixture
def fake_applications(fake_companies):
    attachment = SimpleUploadedFile(name='attachment.txt', 
                    content=b'this is content of uploaded file')

    for i in range(11):
        if i % 2 == 0:
            application = MyApplication(application_type=random.choice(['ASSOC', 'INDEP']),
                                        applied_to=fake_companies,
                                        position=fake.job(),
                                        cover_letter=fake.paragraph(nb_sentences=6)
                                        )
        else:
            application = MyApplication(application_type=random.choice(['ASSOC', 'INDEP']),
                                        applied_to=fake_companies,
                                        position=fake.job(),
                                        attachment=attachment,
                                        comments="Just an random Comment"
                                        )
        application.save()
    return application


@pytest.fixture
def fake_job_offers(fake_applications):
    apps = MyApplication.objects.filter(application_type='ASSOC')
    for app in apps:
        return JobOffer.objects.create(application=app)

@pytest.fixture
def fake_apps_with_tags():
    ...    
