from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from datetime import date
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import *

# from app.models import Article
from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer, VoteForQuestion

# Импортируем формы
from app.forms import LoginForm


def listing(content_list, request, num_per_page):
    paginator = Paginator(content_list, num_per_page)

    page = request.GET.get("page")
    content_list = paginator.get_page(page)
    return content_list


def index(request):
    questions = Question.objects.new_questions()
    content = listing(questions, request, 5)
    return render(request, 'index.html', {'content': content})


def ask(request):

    if request.method == "GET":
        form = AskForm()

    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            tags = form.save()
            profile = Profile.objects.filter(user=request.user).values("id")
            question = Question.objects.create(author_id=profile,
                                               title=form.cleaned_data["title"],
                                               text=form.cleaned_data["text"],
                                               date=datetime.today())
            for _tag in tags:
                question.tags.add(_tag)
                question.save()
            return redirect("question", pk=question.id)
    return render(request, "ask_question.html", {"form": form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('hot'))
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('hot'))


@login_required
def settings(request):
    if request.method == "GET":
        user = request.user
        form = SettingsForm()
        if not user.is_authenticated:
            return HttpResponseForbidden()

    if request.method == "POST":
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated:
                if form.cleaned_data["username"] != user.username and form.cleaned_data["username"] != "":
                    user.username = form.cleaned_data["username"]
                    user.save()
                    auth.login(request, user)
                    # Profile.objects.filter(user=user).update(username=login)
                if form.cleaned_data["email"] != user.email and form.cleaned_data["email"] != "":
                    user.email = form.cleaned_data["email"]
                    user.save()
                    auth.login(request, user)
    return render(request, "settings.html", {"form": form})


def signup(request):
    if request.method == "GET":
        form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                auth.login(request, user)
                return redirect("index")
    return render(request, "signup.html", {"form": form})


def hot(request):
    questions = Question.objects.hot_questions()
    content = listing(questions, request, 5)
    return render(request, 'hot.html', {'content': content})


def tag(request, tag_name):
    questions = Question.objects.tag_questions(tag_name)
    content = listing(questions, request, 5)
    return render(request, 'tag.html', {'content': content, 'tag_name': tag_name})


def single_question(request, pk):

    selected_question = Question.objects.single_question(pk)
    selected_answers = Answer.objects.filter(question=selected_question)
    content = listing(selected_answers, request, 3)

    if request.method == "GET":
        form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        profile = Profile.objects.filter(user=request.user).values("id")
        if form.is_valid():
            answer = Answer.objects.create(question_id=selected_question.id,
                                           author_id=profile,
                                           text=form.cleaned_data["text"])
            return redirect(reverse("question", kwargs={"pk": selected_question.id}) + "?page="
                            + str(content.paginator.num_pages))

    return render(request, "question.html",
                  {"question": selected_question, "content": content, "form": form})
