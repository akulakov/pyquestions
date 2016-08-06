from django.contrib import admin
from .models import *
class QuestionAdmin(admin.ModelAdmin):
    list_display = "question answer choices difficulty created_by".split()

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)
