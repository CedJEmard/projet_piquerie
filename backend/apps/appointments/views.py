from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import Appointment, AvailabilityBlock, Region
from apps.services.models import Service


def get_available_slots(request):
    region_id = request.GET.get('region')
    service_id = request.GET.get('service')
    date_value = request.GET.get('date')

    selected_date = parse_date(date_value)

    if not region_id or not service_id or not selected_date:
        return JsonResponse({'slots': []})

    region = Region.objects.get(id=region_id)
    service = Service.objects.get(id=service_id)

    weekday = selected_date.weekday()

    availability_blocks = AvailabilityBlock.objects.filter(
        weekday=weekday,
        regions=region,
        is_active=True
    )

    existing_appointments = Appointment.objects.filter(
        appointment_date__date=selected_date,
        region=region
    ).exclude(status='cancelled')

    slots = []

    for block in availability_blocks:
        current = datetime.combine(selected_date, block.start_time)
        end = datetime.combine(selected_date, block.end_time)

        current = timezone.make_aware(current)
        end = timezone.make_aware(end)

        while current + timedelta(minutes=service.duration_minutes) <= end:
            slot_start = current
            slot_end = current + timedelta(minutes=service.duration_minutes)

            available = True

            for appointment in existing_appointments:
                existing_start = appointment.appointment_date
                existing_end = existing_start + timedelta(
                    minutes=appointment.service.duration_minutes
                )

                if existing_start < slot_end and existing_end > slot_start:
                    available = False
                    break

            if available:
                slots.append({
                    'value': slot_start.isoformat(),
                    'label': slot_start.strftime('%H:%M')
                })

            current += timedelta(minutes=15)

    return JsonResponse({'slots': slots})


def book_appointment(request):
    services = Service.objects.filter(is_active=True)
    regions = Region.objects.filter(is_active=True)

    if request.method == 'POST':
        service = Service.objects.get(id=request.POST['service'])
        region = Region.objects.get(id=request.POST['region'])

        Appointment.objects.create(
            service=service,
            region=region,
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
            'services': services,
            'regions': regions
        }
    )