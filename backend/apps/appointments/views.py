from django.shortcuts import render, redirect

from .models import Appointment
from apps.services.models import Service


def book_appointment(request):

    services = Service.objects.filter(is_active=True)

    if request.method == 'POST':

        service = Service.objects.get(id=request.POST['service'])

        Appointment.objects.create(
            service=service,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            phone_number=request.POST['phone_number'],
            email=request.POST.get('email', ''),
            address=request.POST['address'],
            appointment_date=request.POST['appointment_date'],
        )

        return redirect('/')

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'services': services
        }
    )