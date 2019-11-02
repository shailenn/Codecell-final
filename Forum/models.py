from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    
    title = models.CharField(max_length = 100, verbose_name = "Title", unique = True, blank = False, null = False)

    description = models.CharField(max_length = 500, verbose_name = "Description", blank = True)

    def __str__(self):
        return self.title

class Forum_question(models.Model):

    question = models.CharField(max_length = 200, verbose_name = "Question Text", unique = True, blank = False, null = False)

    description = models.CharField(max_length = 500, verbose_name = "Question Description", unique = False, blank = True)
    
    topic = models.ManyToManyField(Topic, verbose_name = "Topic")

    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Question Author")

    asked_on = models.DateTimeField(auto_now_add = True, verbose_name = "Asked on ")

    views = models.IntegerField(verbose_name = "Views", default = 0, blank = False, null = False)

    upvotes = models.IntegerField(verbose_name = "Upvotes", default = 0, blank = False, null = False)

    class meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question
    
    def count_answers(self):
        return Forum_answer.objects.all().filter(question = self).count()
    

class Forum_answer(models.Model):

    answer = models.CharField(max_length = 10000, verbose_name = "Answer", blank = False, null = False)
        
    question = models.ForeignKey(Forum_question, on_delete = models.CASCADE, verbose_name = "Question")

    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Author")

    answered_on = models.DateTimeField(auto_now_add = True, verbose_name = "Answered on ")

    views = models.IntegerField(verbose_name = "Views", default = 0, blank = False, null = False)

    upvotes = models.IntegerField(verbose_name = "Upvotes", default = 0, blank = False, null = False)

    def __str__(self):
        return self.answer


class Comment(models.Model):

    comment = models.CharField(max_length = 200, verbose_name = "Comment", blank = False, null = False)

    answer = models.ForeignKey(Forum_answer, on_delete = models.CASCADE, verbose_name = "Answer")

    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Author")

    commented_on = models.DateTimeField(auto_now_add = True, verbose_name = "Asked on ")

    views = models.IntegerField(verbose_name = "Views", default = 0, blank = False, null = False)

    upvotes = models.IntegerField(verbose_name = "Upvotes", default = 0, blank = False, null = False)

    def __str__(self):
        return self.comment