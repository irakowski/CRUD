# Generated by Django 3.1.4 on 2021-01-29 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jboffer', '0009_auto_20210129_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtag',
            name='name',
            field=models.CharField(db_index=True, max_length=150, unique=True, verbose_name='Tags'),
        ),
    ]