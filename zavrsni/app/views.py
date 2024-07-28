from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import RegistrationForm, SurveyForm
from .models import Patient, Doctor, SurveyResponse
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from .utils import map_answers_to_values, generate_recommendation
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def RegisterView(request):
    context = {}
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user.set_password(raw_password)                
            user.save()
            # Create user profile
            isDoctor = form.cleaned_data['isDoctor']
            if isDoctor:
                Doctor.objects.create(user=user, name=username)
            else:
                Patient.objects.create(user=user, name=username)
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

            # Provjeri postoji li već zapis za ovaj datum
            existing_response = SurveyResponse.objects.filter(user=request.user, date=survey_response.date).first()
            if existing_response:
                existing_response.delete()  # Zamijeni postojeći zapis

            survey_response.save()
            
            # generiranje preporuke
            recommendation = generate_recommendation(survey_response)

            return render(request, 'app/recommendation.html', {'recommendation': recommendation})

            # return redirect(reverse('home'))
    else:
        form = SurveyForm()
    return render(request, 'app/survey.html', {'form': form})


@login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    survey_responses = SurveyResponse.objects.filter(user=request.user).order_by('-date')

    context = {
        'patient': patient,
        'survey_responses': survey_responses,
    }

    return render(request, 'app/patient_profile.html', context)

