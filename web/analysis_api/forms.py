from django.forms import ModelForm
from .models import Analysis

class AnalysisForm(ModelForm):
    class Meta:
        model = Analysis
        fields = ['analysis', ]
