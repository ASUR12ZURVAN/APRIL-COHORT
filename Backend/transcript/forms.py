# transcript/forms.py
from django import forms
from .models import CallTranscript

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = CallTranscript
        fields = ['raw_text']
        widgets = {
            'raw_text': forms.Textarea(attrs={'rows': 5})
        }