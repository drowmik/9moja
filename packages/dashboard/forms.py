from django import forms
from main_app.models import Post


class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'img']


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'img']