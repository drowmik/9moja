from django import forms
from django.core.exceptions import ValidationError
from main_app.models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'img', 'status', 'nsfw']


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={
            'required': 'নাম ছাড়া যায়না চেনা!'
        }
    )
    
    class Meta:
        model = Post
        fields = ['title', 'img']
    
    def clean_title(self):
        """
        If somebody enters into this form ' hello ',
        the extra whitespace will be stripped.
        but not space between character
        """
        title = self.cleaned_data.get('title')
        if title:
            return title.rstrip().lstrip()
        else:
            raise ValidationError('নাম ছাড়া যায়না চেনা!')
    
    def clean_img(self):
        img = self.cleaned_data.get('img')
        if img:
            return img
        else:
            raise ValidationError('ছবি বিনা না আসে মজা!')


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = (
            'username',
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            'password2',
        )
