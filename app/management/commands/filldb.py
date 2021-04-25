from django.core.management.base import BaseCommand, CommandError
from random import choice
from itertools import islice
from ...models import *
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # В скобках: (сокращённая запись комманды, полная запись комманды, тип принимаемого параметра)
        parser.add_argument('-u', '--users', type=int)
        parser.add_argument('-t', '--tags', type=int)
        parser.add_argument('-q', '--questions', type=int)
        parser.add_argument('-a', '--answers', type=int)
        parser.add_argument('-vfa', '--votes_for_answers', type=int)
        parser.add_argument('-vfq', '--votes_for_questions', type=int)

    # Типа функция, связывающая команды с аргументами (или нет...)
    def handle(self, *args, **options):
        if options['users']:
            self.fill_users(options['users'])
        if options['tags']:
            self.fill_tags(options['tags'])
        if options['questions']:
            self.fill_questions(options['questions'])
        if options['answers']:
            self.fill_answers(options['answers'])
        if options['votes_for_answers']:
            self.fill_votes_for_answers(options['votes_for_answers'])
        if options['votes_for_questions']:
            self.fill_votes_for_questions(options['votes_for_answers'])

    def fill_tags(self, n):
        for i in range(n):
            Tag.objects.create(name='#' + faker.word() + '_' + faker.word())

    def fill_users(self, n):
        logins = set()

        while len(logins) != n:
            logins.add(faker.word() + '_' + faker.word() + str(faker.random.randint(0, 10000)))

        for login in logins:
            user = User.objects.create(username=login, password=faker.password(), email=faker.email())
            Profile.objects.create(user=user)

    def fill_questions(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('id', flat=True))

        for i in range(n):
            question = Question.objects.create(author_id=choice(users), title=faker.sentence(3) + '?',
                                               text=faker.text(), date=faker.date_between('-50d', 'today'))

            question.tags.add(choice(tags))

    def fill_answers(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        # answers = []

        for i in range(n):
            Answer.objects.create(question_id=choice(questions), author_id=choice(users),
                                  text=faker.sentence())
            # answers.append(answer)

        # Поставить 100 000
        # batch_size = 1
        # while True:
        # batch = list(islice(answers, batch_size))
        # if not batch:
        # break
        # Answer.objects.bulk_create(batch, batch_size)

    def fill_votes_for_questions(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        # votes = []

        for i in range(n):
            _vote = VoteForQuestion.objects.create(question_id=choice(questions),
                                                   author_id=choice(users), vote=faker.random.randint(-1, 1))
            _vote.answer.change_rating(_vote.vote)
            # Не сработало (
            # temp_vote.question.change_rating(temp_vote.vote)

            # votes.append(temp_vote)

        # Поставить 100 000
        # batch_size = 1
        # while True:
        #   batch = list(islice(votes, batch_size))
        #  if not batch:
        #     break
        # VoteForQuestion.objects.bulk_create(batch, batch_size)

    def fill_votes_for_answers(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        answers = list(Answer.objects.values_list('id', flat=True))
        # votes = []

        for i in range(n):
            _vote = VoteForAnswer.objects.create(author_id=choice(users), answer_id=choice(answers),
                                                 vote=faker.random.randint(-1, 1))

            # Почему-то не сработало (
            # _vote.answer.change_rating(_vote.vote)

            # votes.append(_vote)

        # Поставить 100 000
    # batch_size = 1
    # while True:
    #  batch = list(islice(votes, batch_size))
    #   if not batch:
    #     break
    #    Answer.objects.bulk_create(batch, batch_size)
