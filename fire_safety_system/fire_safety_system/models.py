from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Модель пользователя
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # UUID в качестве первичного ключа
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    owned_detectors = models.ManyToManyField('Detector', blank=True, related_name='owners')

    class Meta:
        app_label = 'fire_safety_system'  # Указываем app_label

    def __str__(self):
        return self.username

# Модель датчика
class Detector(models.Model):
    detector_id = models.CharField(max_length=100, unique=True) # Уникальный идентификатор датчика
    location = models.CharField(max_length=255) # Местоположение датчика
    status = models.CharField(max_length=50, default='active') # Статус датчика (например, "active", "inactive", "error")

    class Meta:
        app_label = 'fire_safety_system'  # Указываем app_label

    def __str__(self):
        return f"{self.detector_id} - {self.location}"