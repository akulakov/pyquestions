from .models import *
from django.forms import *
from django.contrib.auth.models import User
from random import shuffle

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "question answer choices difficulty question_type version".split()
        widgets = dict(
                question=TextInput(attrs=dict(size=150)),
                answer=TextInput(attrs=dict(size=150)),
                choices=TextInput(attrs=dict(size=150)),
                )

class UpdateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "question answer choices difficulty question_type reviewed flagged version".split()
        widgets = dict(
                question=TextInput(attrs=dict(size=150)),
                answer=TextInput(attrs=dict(size=150)),
                choices=TextInput(attrs=dict(size=150)),
                )

class QuestionForm(Form):
    def __init__(self, question=None, *a, **kw):
        super(QuestionForm, self).__init__(*a, **kw)
        choices = [x.strip() for x in question.choices.split('|')]
        shuffle(choices)
        kw = dict(help_text=question.question)
        self.is_radio=0

        if any(choices):
            fld = ChoiceField
            #choices = [c.strip() for c in choices.split(',')]
            kw["choices"] = [(c,c) for c in choices]
            kw["widget"] = RadioSelect()
            self.is_radio=1
        else:
            fld = CharField
            kw["max_length"] = 100

        self.fields["answer"] = fld(**kw)
    #answer = CharField(max_length=100)
