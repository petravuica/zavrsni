from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import RegistrationForm, SurveyForm, MessageForm
from .models import Patient, Doctor, SurveyResponse, Message
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from .utils import DISEASE_SYMPTOM_WEIGHTS, generate_probabilities, generate_recommendation, generate_top_n_recommendations, get_recommendations_for_condition, map_answers_to_values
from django.contrib.auth.decorators import login_required, user_passes_test
from io import BytesIO
import base64
# Create your views here.
import matplotlib
matplotlib.use('Agg')  # Koristi backend koji ne zahtijeva GUI
import matplotlib.pyplot as plt


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
            # Generiraj preporuke i popis najvjerojatnijih bolesti
            recommendations, top_diseases = generate_top_n_recommendations(survey_response, n=3)

            survey_response.recommendation = '\n'.join(recommendations)
            survey_response.save()

            return render(request, 'app/recommendation.html', {
                'recommendations': recommendations,
                'top_diseases': top_diseases,
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
    
    
    context = {
        'patient': patient,
        'survey_responses': survey_responses,
        'recommendations': recommendations,
        'messages': messages,
        'form': form
        
    }

    return render(request, 'app/patient_profile.html', context)


def is_doctor(user):
    return Doctor.objects.filter(user=user).exists()

user_passes_test(is_doctor)
@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('user__last_name', 'name')
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

def plot_survey_results(request):
    # Dohvati sve ankete za trenutnog korisnika
    survey_responses = SurveyResponse.objects.filter(user=request.user).order_by('date')

    # Ako nema anketa, vrati praznu sliku
    if not survey_responses:
        return HttpResponse("No survey responses available.")

    # Pripremi podatke za dijagram
    dates = [response.date for response in survey_responses]
    probabilities = {disease: [] for disease in DISEASE_SYMPTOM_WEIGHTS.keys()}

    for response in survey_responses:
        values = map_answers_to_values(response)
        probs = generate_probabilities(values)
        for disease in probabilities:
            probabilities[disease].append(probs[disease])

    # Stvaranje linijskog dijagrama
    plt.figure(figsize=(10, 6))
    for disease, probs in probabilities.items():
        plt.plot(dates, probs, label=disease)

    plt.xlabel('Datum')
    plt.ylabel('Vjerojatnost')
    plt.title('Vjerojatnosti bolesti kroz vrijeme')
    plt.legend()
    plt.grid(True)

    # Spremi dijagram u memoriju kao sliku
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render(request, 'app/survey_results.html', {'image': img_str})