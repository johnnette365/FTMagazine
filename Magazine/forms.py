from django import forms
from .models import Comment, Subscriber





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'input-field', 'required': True}),
        }