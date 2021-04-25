from django.db import models
from django.contrib.auth.models import User


############################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="../static/img/pic.png")

    def __str__(self):
        return self.user.username


class QuestionsManager(models.Manager):
    def new_questions(self):
        return self.order_by('date')

    def hot_questions(self):
        return self.order_by('-rating')

    def tag_questions(self, tag_name):
        tag = Tag.objects.filter(name=tag_name)
        return self.filter(tags__in=tag)

    def single_question(self, pk):
        # Важно, чтобы возвращался объект, а не множество объектов.
        return self.filter(id=pk).first()


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)
    date = models.DateField()

    objects = QuestionsManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def change_rating(self, rate):
        if rate:
            self.rating += 1
        else:
            self.rating -= 1


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return 'Answer on '+self.question.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def change_rating(self, rate):
        if rate:
            self.rating += 1
        else:
            self.rating -= 1


class VoteForAnswer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    UNVOTED = 0
    vote_types = [(LIKE, 'Like'), (DISLIKE, 'Dislike'), (UNVOTED, 'Unvoted')]

    vote = models.SmallIntegerField(choices=vote_types, default=UNVOTED)

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + ' --> answer#'+str(self.answer.id)

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответа'


class VoteForQuestion(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    UNVOTED = 0
    vote_types = [(LIKE, 'Like'), (DISLIKE, 'Dislike'), (UNVOTED, 'Unvoted')]

    vote = models.SmallIntegerField(choices=vote_types, default=UNVOTED)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + ' --> question#'+str(self.question.id)

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'
