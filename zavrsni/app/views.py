from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import RegistrationForm, SurveyForm, MessageForm
from .models import Patient, Doctor, SurveyResponse, Message
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from .utils import generate_probabilities, generate_top_n_recommendations, map_answers_to_values, generate_recommendation
from django.contrib.auth.decorators import login_required, user_passes_test
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def RegisterView(request):
    context = {}
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['firstName']
            user.last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user.set_password(raw_password)                
            user.save()
            # Create user profile
            gender = form.cleaned_data['gender']
            dateOfBirth = form.cleaned_data['dateOfBirth']
            isDoctor = form.cleaned_data['isDoctor']
            if isDoctor:
                Doctor.objects.create(user=user, name=username, gender=gender, dateOfBirth=dateOfBirth)
            else:
                Patient.objects.create(user=user, name=username, gender=gender, dateOfBirth=dateOfBirth)
            # Authenticate and login user
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            if not form.errors:
                form.add_error(field=None, error='Passwords do not match.')
    else:
        form = RegistrationForm()
    
    context['form'] = form
    return render(request, 'registration/register.html', context)

def SurveyView(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey_response = form.save(commit=False)
            survey_response.user = request.user

            survey_response.save()
            # Generiraj top 3 preporuke
            recommendations = generate_top_n_recommendations(survey_response, n=3)

            
            survey_response.recommendation = recommendations
            survey_response.save()

            return render(request, 'app/recommendation.html', {
                'recommendations': recommendations,   
            })
            
    else:
        form = SurveyForm()
    return render(request, 'app/survey.html', {'form': form})

def user_type(request):
    if request.user.is_authenticated:
        if Patient.objects.filter(user=request.user).exists():
            return {'user_type': 'patient'}
        elif Doctor.objects.filter(user=request.user).exists():
            return {'user_type': 'doctor'}
    return {'user_type': None}

@login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    survey_responses = SurveyResponse.objects.filter(user=request.user).order_by('-date')

    recommendations = {}
    for response in survey_responses:
        recommendation = generate_recommendation(response)
        recommendations[response.id] = recommendation
    
    # Prikaz poruka
    messages = Message.objects.filter(recipient=request.user).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = patient.user
            message.save()
            return redirect('patient_profile')
    else:
        form = MessageForm()
    
    graph = plot_survey_results(survey_responses)
    context = {
        'patient': patient,
        'survey_responses': survey_responses,
        'recommendations': recommendations,
        'messages': messages,
        'form': form,
        'graph': graph
        
    }

    return render(request, 'app/patient_profile.html', context)


def is_doctor(user):
    return Doctor.objects.filter(user=user).exists()

user_passes_test(is_doctor)
@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('name')
    return render(request, 'app/patient_list.html', {'patients': patients})

@user_passes_test(is_doctor)
@login_required
def PatientDetail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    survey_responses = SurveyResponse.objects.filter(user=patient.user).order_by('-date')
    
    recommendations = {}
    for response in survey_responses:
        recommendation = generate_recommendation(response)
        recommendations[response.id] = recommendation
    
    # Prikupiti sve poruke između liječnika i pacijenta
    messages = Message.objects.filter(sender=request.user, recipient=patient.user) | Message.objects.filter(sender=patient.user, recipient=request.user)
    messages = messages.order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = patient.user
            message.save()
            return redirect('patient_detail', patient_id=patient_id)
    else:
        form = MessageForm()
    
    context = {
        'patient': patient,
        'survey_responses': survey_responses,
        'recommendations': recommendations,
        'form': form,
        'messages': messages,
    }

    return render(request, 'app/patient_detail.html', context)

def plot_survey_results(survey_responses):
    # Ovde možete prilagoditi podatke iz anketa koje želite prikazati na grafu
    dates = [response.date for response in survey_responses]
    heartburn_data = [response.heartburn for response in survey_responses]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, heartburn_data, marker='o', color='b', label='Heartburn')
    
    # Dodaj više linija ako želiš pratiti više odgovora
    plt.xlabel('Datum')
    plt.ylabel('Rezultat')
    plt.title('Praćenje rezultata ankete kroz vrijeme')
    plt.legend()
    plt.grid(True)

    # Spremaj grafiku u memorijski buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Enkodiraj grafiku u base64 format kako bi je mogli prikazati u HTML-u
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close('all')
    return graph