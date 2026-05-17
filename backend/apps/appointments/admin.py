from django.contrib import admin

from .models import (
    Appointment,
    Region,
    AvailabilityBlock
)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'appointment_date',
        'service',
        'region',
        'status',
    )

    list_filter = (
        'status',
        'service',
        'region',
        'appointment_date',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'name',
    )


@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):

    list_display = (
        'weekday',
        'start_time',
        'end_time',
        'is_active',
    )

    list_filter = (
        'weekday',
        'is_active',
    )

    filter_horizontal = (
        'regions',
    )