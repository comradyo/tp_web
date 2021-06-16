from django import forms
from .models import *
from django.contrib import auth


# ==================================================================
class LoginForm(forms.Form):
    # По умолчанию required = True
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


# ==================================================================
class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "username"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "abc@mail.ru"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Enter password"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm password"}))

    avatar = forms.ImageField(required=False, widget=forms.FileInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            self.add_error(None, "Passwords do not match!")

    def save(self):
        user = User.objects.create(username=self.cleaned_data.get("username"),
                                   password=self.cleaned_data.get("password"),
                                   email=self.cleaned_data.get("email"))
        Profile.objects.create(user=user, login=user.username)
        return user


# ========================================================================
class SettingsForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput())
    email = forms.EmailField(required=False, widget=forms.EmailInput())
    avatar = forms.ImageField(required=False, widget=forms.FileInput())


# =========================================================================

class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "How?"}))
    text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "And why?", "rows": 8}))
    tags = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "SQL, C++"}))

    def save(self):
        tags = []
        for tag in self.cleaned_data["tags"].split(','):
            tags.append(tag.strip())
        tag_list = []
        for tag in tags:
            t = Tag.objects.filter(name=tag).first()
            if t is None:
                t = Tag.objects.create(name=tag)
            else:
                t.save()
            tag_list.append(t)
        return tag_list


# ================================================================
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter your answer here"}), label="")
