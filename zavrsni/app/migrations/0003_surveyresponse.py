# Generated by Django 4.2 on 2024-07-18 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_remove_patient_address_remove_patient_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('therapy', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'M'), ('Ž', 'Ž')], max_length=1)),
                ('smoking', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('alcohol', models.CharField(choices=[('Nikad', 'Nikad'), ('Rijetko', 'Rijetko'), ('Često', 'Često')], max_length=7)),
                ('heartburn', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('chest_pain', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('dysphagia', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('h_pylori', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('nsaids', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('abdominal_pain', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('nausea_vomiting', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('postprandial_pain', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('diarrhea', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('cramps', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('fatigue_anemia', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('urgency', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('weight_loss', models.CharField(choices=[('Da', 'Da'), ('Ne', 'Ne')], max_length=3)),
                ('stress', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('appetite_loss', models.CharField(choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')], max_length=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
