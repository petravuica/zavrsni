from django import forms
from .models import Patient,Doctor, SurveyResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    firstName = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First name'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm password'}))
    isDoctor = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input', }), required=False)

    class Meta:
        model = User
        fields = ['username', 'firstName', 'lastName', 'email', 'password1', 'password2', 'isDoctor']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error(None, "This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error(None, "This email address is already taken.")
        return email

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = [
            'therapy',
            'age',
            'gender',
            'smoking',
            'alcohol',
            'heartburn',
            'chest_pain',
            'dysphagia',
            'h_pylori',
            'nsaids',
            'abdominal_pain',
            'nausea_vomiting',
            'postprandial_pain',
            'diarrhea',
            'cramps',
            'fatigue_anemia',
            'urgency',
            'weight_loss',
            'stress',
            'appetite_loss'
        ]
        widgets = {
            'therapy': forms.RadioSelect,
            'gender': forms.RadioSelect,
            'smoking': forms.RadioSelect,
            'alcohol': forms.RadioSelect,
            'heartburn': forms.RadioSelect,
            'chest_pain': forms.RadioSelect,
            'dysphagia': forms.RadioSelect,
            'h_pylori': forms.RadioSelect,
            'nsaids': forms.RadioSelect,
            'abdominal_pain': forms.RadioSelect,
            'nausea_vomiting': forms.RadioSelect,
            'postprandial_pain': forms.RadioSelect,
            'diarrhea': forms.RadioSelect,
            'cramps': forms.RadioSelect,
            'fatigue_anemia': forms.RadioSelect,
            'urgency': forms.RadioSelect,
            'weight_loss': forms.RadioSelect,
            'stress': forms.RadioSelect,
            'appetite_loss': forms.RadioSelect,
        }
        labels = {
            'therapy': 'Primate li terapiju?',
            'age': 'Koliko imate godina?',
            'gender': 'Spol',
            'smoking': 'Konzumirate li cigarete?',
            'alcohol': 'Konzumirate li alkohol?',
            'heartburn': 'Imate li osjećaj žgaravice (osjećaj vraćanja kisele tekućine u grlo ili usta)?',
            'chest_pain': 'Imate li neprekidnu bol u sredini prsa koja se širi prema leđima?',
            'dysphagia': 'Imate li poteškoće tijekom gutanja (disfagiju)?',
            'h_pylori': 'Jeste li ikad imali dijagnozu infekcije bakterije Helicobacter pylori?',
            'nsaids': 'Koristite li često nesteroidne antireumatike (npr. aspirin, ibuprofen)',
            'abdominal_pain': 'Imate li bolove u trbuhu ili nadutost?',
            'nausea_vomiting': 'Imate li osjećaj mučnine i povraćate li?',
            'postprandial_pain': 'Osjećate li bol u gornjem dijelu trbuha nakon jela?',
            'diarrhea': 'Patite li od proljeva?',
            'cramps': 'Osjećate li grčeve u trbuhu, posebno u donjem desnom dijelu?',
            'fatigue_anemia': 'Jeste li umorni i imate li anemiju?',
            'urgency': 'Imate li osjećaj hitnosti za odlazak na toalet?',
            'weight_loss': 'Gubite li težinu bez ikakvog razloga?',
            'stress': 'Jeste li pod stresom?',
            'appetite_loss': 'Imate li osjećaj gubitka apetita i punoće?',
        }
        def __init__(self, *args, **kwargs):
            super(SurveyForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.RadioSelect):
                    field.choices = field.choices[1:]

