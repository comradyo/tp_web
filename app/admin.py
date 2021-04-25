from django.contrib import admin

# Register your models here.

from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer
from app.models import VoteForQuestion

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(VoteForAnswer)
admin.site.register(VoteForQuestion)
