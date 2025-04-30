from django.db import models

class HealthSymptom(models.Model):
    """Model for health symptoms (placeholder for the external database)"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Health Symptom"
        verbose_name_plural = "Health Symptoms" 