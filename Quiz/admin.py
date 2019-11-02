from django.contrib import admin
from Quiz.models import *
from Quiz.MultipleChoice.models import *


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuizAdmin(admin.ModelAdmin):
    #form = QuizAdminForm  # need to be added 
    list_display = ('title','category',)
    list_filter = ('category',)
    search_fields = ('description','category')

class MCQAdmin(admin.ModelAdmin):
    list_display = ('content','category',)
    list_filter = ('category',)
    fields = ('content','category','figure','quiz','explanation','answer_order')
    search_fields = ('content','explanation')
    filter_horizontal = ('quiz',)
    inlines = [AnswerInline]


# Register your models here.

admin.site.register(Category,CategoryAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(MCQ,MCQAdmin)
admin.site.register(Progress)