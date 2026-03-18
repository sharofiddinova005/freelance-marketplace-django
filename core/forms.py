from django import forms
from .models import Project, Bid

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'deadline']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'message']