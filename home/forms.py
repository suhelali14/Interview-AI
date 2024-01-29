# forms.py
from django import forms
from .models import AudioRecording

class AudioRecordingForm(forms.ModelForm):
    class Meta:
        model = AudioRecording
        fields = ['name', 'audio_file']