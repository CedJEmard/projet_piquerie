from django.db import models


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Confirmé'),
        ('completed', 'Complété'),
        ('lab_processing', 'En analyse'),
        ('sent_to_doctor', 'Transmis au médecin'),
        ('cancelled', 'Annulé'),
    ]

    patient_profile = models.ForeignKey(
        'patients.PatientProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )

    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    address = models.TextField()

    appointment_date = models.DateTimeField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='confirmed'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date}"