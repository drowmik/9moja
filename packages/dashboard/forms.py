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



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
