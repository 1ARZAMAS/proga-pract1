from django import forms
from .models import Detector

class DetectorForm(forms.ModelForm):
    class Meta:
        model = Detector
        fields = ['detector_id', 'location', 'status']