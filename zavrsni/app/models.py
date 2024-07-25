from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    therapy = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=[('M', 'M'), ('Ž', 'Ž')])
    smoking = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    alcohol = models.CharField(max_length=7, choices=[('Nikad', 'Nikad'), ('Rijetko', 'Rijetko'), ('Često', 'Često')])
    heartburn = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    chest_pain = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    dysphagia = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    h_pylori = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    nsaids = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    abdominal_pain = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    nausea_vomiting = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    postprandial_pain = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    diarrhea = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    cramps = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    fatigue_anemia = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    urgency = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    weight_loss = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    stress = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
    appetite_loss = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])

    def __str__(self):
        return f"SurveyResponse {self.id} for {self.user.username} on {self.date}"


