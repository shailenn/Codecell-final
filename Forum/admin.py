from django.contrib import admin
from Forum.models import *

# Register your models here.

admin.site.register(Topic)
admin.site.register(Forum_question)
admin.site.register(Forum_answer)
admin.site.register(Comment)