from django.db import models


class MedicalDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('prescription', 'Prescription / requête médicale'),
        ('photo', 'Photo'),
        ('other', 'Autre document'),
    ]

    patient_profile = models.ForeignKey(
        'patients.PatientProfile',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        default='prescription'
    )

    file = models.FileField(
        upload_to='medical_documents/'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.patient_profile}"