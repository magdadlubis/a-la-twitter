from django import forms
from .models import Tweet, Comment, UserModel, Message


class AddTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adres e-mail')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    email = forms.EmailField(label='Adres e-mail')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class EditUserForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Password')
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']