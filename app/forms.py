from django import forms


class LoginForm(forms.Form):
    # По умолчанию required = True
    username = forms.CharField()
    password = forms.CharField()
