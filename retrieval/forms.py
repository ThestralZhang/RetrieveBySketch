from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    email = forms.EmailField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput())
    password = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput())


class UploadFileForm(forms.Form):
    img = forms.ImageField()
    tag1 = forms.CharField(max_length=50, required=False, label='tag1(Optional)')
    tag2 = forms.CharField(max_length=50, required=False, label='tag2(Optional')
    tag3 = forms.CharField(max_length=50, required=False, label='tag3(Optional)')
