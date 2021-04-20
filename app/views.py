from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

questions = [
    {
        'image': "static/img/pic1.jpg",
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}',
        'tags': f'tag_{idx}'
    } for idx in range(10)
]


def listing(content_list, request, num_per_page):
    paginator = Paginator(content_list, num_per_page)  # Show 4 questions per page

    page = request.GET.get("page")
    content_list = paginator.get_page(page)
    return content_list


def index(request):
    content = listing(questions, request, 4)
    return render(request, 'index.html', {'content': content})


def ask(request):
    return render(request, 'ask_question.html', {})


def login(request):
    return render(request, 'login.html', {})


answers = [
    {
        'text': f'Answer text #{idx}'
    } for idx in range(20)
]

def single_question(request, pk):
    question = questions[pk]
    content = listing(answers, request, 10)
    return render(request, 'question.html', {"question": question, "content": content})


def settings(request):
    return render(request, 'settings.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def hot(request):
    content = listing(questions, request, 4)
    return render(request, 'hot.html', {'content': content})


def tag(request, tag_name):
    return render(request, 'tag.html', {"tag": tag_name})
