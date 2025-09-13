from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'نظر شما', 'cols':'30', 'rows':'6'})
        }
        labels = {
            'body': False
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'پاسخ شما', 'cols':'30', 'rows':'2'})
        }
        labels = {
            'body': False
        }