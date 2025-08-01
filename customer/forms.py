from django import forms
from .models.feedback import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Write your feedback here...', 'rows': 4}),
            'rating': forms.RadioSelect(),
        }
        labels = {
            'message': 'Your Feedback',
            'rating': 'Rating',
        }
