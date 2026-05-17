"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from apps.appointments.views import book_appointment
from apps.services.models import Service
from django.contrib.auth.decorators import login_required
from apps.documents.models import MedicalDocument


def home(request):
    services = Service.objects.filter(is_active=True)

    return render(
        request,
        'home.html',
        {
            'services': services
        }
    )
    
@login_required
def account_view(request):
    patient = getattr(request.user, 'patient_profile', None)

    appointments = []
    documents = []

    if patient:
        appointments = patient.appointments.all()

    return render(
        request,
        'account.html',
        {
            'patient': patient,
            'appointments': appointments,
            'documents': documents,
        }
    )
    
@login_required
def add_document_view(request):

    patient = getattr(request.user, 'patient_profile', None)

    if not patient:
        return redirect('/mon-compte/')

    if request.method == 'POST':

        uploaded_file = request.FILES.get('file')

        document_type = request.POST.get('document_type')

        if uploaded_file:

            MedicalDocument.objects.create(
                patient_profile=patient,
                document_type=document_type,
                file=uploaded_file
            )

            return redirect('/mon-compte/')

    return redirect('/mon-compte/')

def edit_account_view(request):

    patient = getattr(request.user, 'patient_profile', None)

    if request.method == 'POST' and patient:

        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.phone_number = request.POST.get('phone_number')
        patient.address = request.POST.get('address')

        patient.save()

        return redirect('/mon-compte/')

    return render(
        request,
        'edit_account.html',
        {
            'patient': patient
        }
    )


def redirect_user_after_login(request):
    if request.user.is_staff:
        return redirect('/admin/')

    return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', home, name='home'),

    path(
        'prendre-rendez-vous/',
        book_appointment,
        name='book_appointment'
    ),

    path(
        'redirect/',
        redirect_user_after_login,
        name='redirect_user_after_login'
    ),
    path(
    'mon-compte/',
    account_view,
    name='account'
    ),
    path(
    'mon-compte/modifier/',
    edit_account_view,
    name='edit_account'
    ),
    path(
    'mon-compte/document/ajouter/',
    add_document_view,
    name='add_document'
    ),
]