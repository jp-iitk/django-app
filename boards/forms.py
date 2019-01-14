from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'rows' : 7,
                'placeholder' : 'What is on your mind?'
            }
        ),
        help_text="Max length of message is 5000 characters",
        required=True,
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
