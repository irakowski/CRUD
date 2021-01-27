# Generated by Django 3.1.4 on 2021-01-26 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jboffer', '0002_auto_20210126_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='company_url',
            new_name='url',
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='myapplication',
            name='application_type',
            field=models.CharField(choices=[('INDEP', 'Independent'), ('ASSOC', 'Associated')], default='INDEP', max_length=5),
        ),
    ]
