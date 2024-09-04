from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Muški'),
        ('F', 'Ženski')
    ], default='M')
    dateOfBirth = models.DateField(default='2000-01-01')	
    

    def __str__(self):
        return f"{self.id} - {self.user.first_name} {self.user.last_name}"
    
class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Muški'),
        ('F', 'Ženski')
    ], default='M')
    dateOfBirth = models.DateField(default='2000-01-01')

    def __str__(self):
        return f"{self.id} - {self.user.first_name} {self.user.last_name}"
    
class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    smoking = models.CharField(max_length=3, choices=[('Da', 'Da'), ('Ne', 'Ne')])
    alcohol = models.CharField(max_length=7, choices=[('Često', 'Često'), ('Ponekad', 'Ponekad'), ('Rijetko', 'Rijetko'), ('Nikad', 'Nikad')])
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
    recommendation = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"SurveyResponse {self.id} for {self.user.username} on {self.date}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'