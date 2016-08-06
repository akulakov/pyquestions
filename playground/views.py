from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import FormView, UpdateView, CreateView, TemplateView
from django.db.models import Q
from .models import *
from .forms import *
from random import random
import random

"""
-style the templates nicely
-log of question updates
-add tags widget and handling
-add ratings
-add comments
-add 'flagged', filter them out

-add download of CSV
-create github proj
"""

class Home(TemplateView):
    template_name = "playground/home.html"

class NewQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = CreateQuestionForm
    template_name = "playground/new_question.html"

    def form_valid(self, form):
        q=form.save(commit=False)
        q.created_by=self.request.user
        if not q.version:
            if q.question_type == "python":
                q.version = "python-3.5"
            if q.question_type == "django":
                q.version = "django-1.9"
        q.save()

        self.q=q
        return self.get_success_url()

    def get_success_url(self):
        messages.success(self.request, "New Question (id=%d) was added successfully" % self.q.pk)
        return redirect(reverse("new_question"))


class UpdateUsernameView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsernameForm
    template_name = "playground/update_username.html"
    success_url = '/'

    def get_object(self):
        return self.request.user

class ReviewRandomQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = UpdateQuestionForm
    template_name = "playground/review.html"

    def Xget_context_data(self, **kw):
        comment_form = AddCommentForm()
        kw.update(dict(comment_form=comment_form))
        return kw

    def get_object(self):
        #for q in Question.objects.all():
        #    q.created_by=User.objects.get(username='ak'); q.save()
        pk = self.request.GET.get("question")
        q = None
        if pk:
            q = Question.objects.get(pk=pk)
        if not q:
            l1 = Question.objects.filter(Q(difficulty__isnull=True) | Q(reviewed=False))
            if l1.exists() and random.random()>.25:
                q = l1.order_by('?').first()
            else:
                q = Question.objects.all().order_by('?').first()
        return q

    def form_valid(self, form):
        q=form.save(commit=False)
        q.last_updated_by=self.request.user; q.save()
        return self.get_success_url()

    def get_success_url(self):
        messages.success(self.request, "Question was updated successfully")
        return redirect(reverse("review_question"))


class RandomQuestionView(FormView):
    template_name = "playground/question.html"

    def get(self, request, *a, **kw):
        id = request.GET.get("question")
        answered=()
        n_answered=0
        if request.user.is_authenticated():
            answered = request.user.userprofile.answered_questions.all()
            n_answered = answered.count()
        if id:
            q = Question.objects.get(pk=id)
        else:
            q = Question.objects.exclude(flagged=True, pk__in=answered).order_by('?').first()
        #print(q, q.choices)
        if not q:
            return HttpResponse("You have already answered all questions. Check back later!")
        request.session['last_question'] = q.pk
        form = QuestionForm(question=q)
        n_questions = Question.objects.filter(flagged=False).count()
        return self.render_to_response(dict(question=q, form=form, n_questions=n_questions,
            n_answered=n_answered, view=self))

    def post(self, request, *a, **kw):
        q = request.session.get('last_question')
        q = Question.objects.get(pk=q)
        #print(q, q.choices)
        c = q.choices
        if c:
            answer = [c[:c.find('|')].strip()]
        else:
            answer = [a.strip() for a in q.answer.split('|')]
        form = QuestionForm(request.POST, question=q)
        if form.is_valid() and form.cleaned_data["answer"] in answer:
            request.user.userprofile.answered_questions.add(q)
            messages.success(request, "Right answer!")
            return redirect(reverse("random_question"))
        else:
            messages.error(request, "Wrong answer, try again..")
            return redirect(reverse("random_question") + '?' + 'question=%s' % q.pk)
