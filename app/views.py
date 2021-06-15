from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from datetime import date

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
    return render(request, 'ask_question.html', {})


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


def settings(request):
    return render(request, 'settings.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def hot(request):
    questions = Question.objects.hot_questions()
    content = listing(questions, request, 5)
    return render(request, 'hot.html', {'content': content})


def tag(request, tag_name):
    questions = Question.objects.tag_questions(tag_name)
    content = listing(questions, request, 5)
    return render(request, 'tag.html', {'content': content, 'tag_name': tag_name})


def single_question(request, pk):
    # .select_related() не работает
    selected_question = Question.objects.single_question(pk)
    selected_answers = Answer.objects.filter(question=selected_question)
    content = listing(selected_answers, request, 3)
    return render(request, 'question.html', {'question': selected_question, 'content': content})
