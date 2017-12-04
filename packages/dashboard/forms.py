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

    def clean_title(self):
        """
        If somebody enters into this form ' hello ',
        the extra whitespace will be stripped.
        but not space between character
        """
        return self.cleaned_data.get('title', '').rstrip().lstrip()
