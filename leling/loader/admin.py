from django.contrib import admin

# Register your models here.
from .models import *


class QuestionType_inline(admin.TabularInline):
    model = QuestionType
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionType_inline,)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Type)
admin.site.register(QuestionType)
