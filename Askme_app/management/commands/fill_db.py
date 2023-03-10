import random
from random import randint
from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from Askme_app.management.commands.logger import make_logger
from Askme_app.models import Question, Vote, Answer, Profile, Tag
from Askme_app.management.commands.random_getter import get_random
from django.utils.datetime_safe import datetime
from Askme_app.models import avatars
# from Askme_app.management.commands import generate_questions, generate_answers, generate_tags, generate_votes, generate_users


class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        start_time = datetime.now().timestamp()
        logger = make_logger(options['debug'])

        ratio = options['ratio']
        faker = Faker()

        # Users
        i = 0
        while i < ratio:
            try:
                username = faker.user_name()
                user = Profile(username=username, login=faker.first_name(), email=faker.email(),
                               password=faker.password(), avatar=random.choice(avatars))
                user.save()
                i += 1
            except IntegrityError:
                logger.warning('User already exists.')


        # Tags
        i = 0
        while i < ratio:
            tag_name = faker.word()[:15]
            tag = Tag.objects.create_or_update_tag(tag=tag_name)
            tag.save()
            i += 1


        # Questions
        i = 0
        while i < ratio*10:
            user = get_random(Profile)
            tags = get_random(Tag, randint(1, 4))

            question = Question(user=user, title=faker.text(max_nb_chars=50),
                                text=faker.text(max_nb_chars=450, ext_word_list=None))
            question.save()
            user.activity +=1
            user.save(update_fields=['activity'])
            if type(tags) == list:
                for tag in tags:
                    tag.total += 1
                    tag.save(update_fields=['total'])
                    question.tags.add(tag)
                    i += 1
            else:
                tags.total += 1
                tags.save(update_fields=['total'])
                question.tags.add(tags)
                i += 1


        # Answers
        i = 0
        while i < ratio*100:
            user = get_random(Profile)
            question = get_random(Question)
            answer = Answer.objects.create_answer(user=user, question=question,
                                                  text=faker.text(max_nb_chars=450, ext_word_list=None),
                                                  is_correct=bool(random.getrandbits(1)))
            answer.save()
            i += 1
            user.activity +=1
            user.save(update_fields=['activity'])



        # Votes
        objects_list = ['questions', 'answers']
        i = 0
        while i < ratio*200:
            try:
                obj_name = random.choice(objects_list)
                user = get_random(Profile)
                if obj_name == 'question':
                    obj = get_random(Question)
                else:
                    obj = get_random(Answer)
                vote = Vote.objects.create_vote(user=user, obj=obj, object_id=obj.id)
                vote.save()
                i += 1
            except IntegrityError:
                logger.warning('Vote already exists.')

        logger.info('Operation executed in {} seconds'.format(datetime.now().timestamp() - start_time))
