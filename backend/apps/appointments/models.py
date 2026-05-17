from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AvailabilityBlock(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]

    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    regions = models.ManyToManyField(
        Region,
        related_name='availability_blocks'
    )

    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time} - {self.end_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmé'),
        ('completed', 'Complété'),
        ('lab_processing', 'En analyse'),
        ('sent_to_doctor', 'Transmis au médecin'),
        ('cancelled', 'Annulé'),
    ]

    CONTACT_PREFERENCE_CHOICES = [
        ('email', 'Courriel'),
        ('sms', 'Texto'),
        ('phone', 'Téléphone'),
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

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='appointments',
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    contact_preference = models.CharField(
        max_length=20,
        choices=CONTACT_PREFERENCE_CHOICES,
        default='phone'
    )

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