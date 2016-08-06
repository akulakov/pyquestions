from __future__ import unicode_literals

from django.db.models import Count, Min, Sum, Avg

from django.db import models
from django.db.models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Comment(Model):
    user = ForeignKey(User, blank=True)
    question = ForeignKey("Question", blank=True, related_name="comments")
    body = CharField(max_length=2000)
    created = DateTimeField(auto_now_add=True)

class Rating(Model):
    user = ForeignKey(User, blank=True, related_name="ratings")
    question = ForeignKey("Question", blank=True, related_name="ratings")
    rating = IntegerField(help_text="0-10")

class Tag(Model):
    created_by = ForeignKey(User, blank=True)
    tag = CharField(max_length=30)

class Question(Model):
    qchoices=(('python', 'python'), ('django','django'), ('vim','vim'))
    vchoices="python-2.7 python-3.5 django-1.9".split()
    vchoices=((c,c) for c in vchoices)

    question = CharField(max_length=4000)
    question_type = CharField(choices=qchoices, max_length=60, default='python', blank=True)
    version = CharField(choices=vchoices, max_length=10, blank=True)
    answer = CharField(max_length=100, blank=True, null=True)
    choices = CharField(max_length=600,
        help_text="separate with pipe sybmol '|', first answer is the correct one, answers will be randomized when question is asked",
        blank=True, null=True)
    difficulty = IntegerField(help_text="0-10, from easiest to hardest", blank=True, null=True)
    reviewed = BooleanField(default=False, help_text="full review of all fields is completed")
    flagged = BooleanField(default=False,
        help_text="Question or answers are incorrect, should be hidden until fixed.")
    tags = ManyToManyField(Tag, related_name="questions", blank=True)
    created_by = ForeignKey(User, blank=True, null=True, related_name="created_questions")
    last_updated_by = ForeignKey(User, blank=True,null=True, related_name="last_updated_questions")

    def rating(self):
        q=Question.objects.filter(pk=self.pk).aggregate(average_rating=Avg('ratings__rating'))
        return q.average_rating

    def __repr__(self):
        return self.question[:70]
    __str__=__repr__

class UserAnswer(Model):
    user = ForeignKey(User, related_name="answers")
    question = ForeignKey(Question, related_name="answers")
    correct = BooleanField()
    answer = CharField(max_length=100, blank=True, null=True)

class UserProfile(Model):
    user = OneToOneField(User)
    answered_questions = ManyToManyField(Question, blank=True)

    def __str__(self):
        return str(self.user)

def user_created(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(user_created, sender=User)
