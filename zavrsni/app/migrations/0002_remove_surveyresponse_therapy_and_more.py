# Generated by Django 4.2 on 2024-08-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyresponse',
            name='therapy',
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='alcohol',
            field=models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7),
        ),
    ]
