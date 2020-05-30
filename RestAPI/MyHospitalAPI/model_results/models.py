from django.db import models

# Create your models here.

class Results(models.Model):
    provider_id = models.CharField(max_length=100, blank=True, default='')
    measure_id = models.CharField(max_length=100, blank=True, default='')
    performance_class = models.CharField(max_length=100, blank=True, default='')