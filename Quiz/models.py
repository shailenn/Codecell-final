import re   # regex for urls
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from Accounts.models import Student


# Create your models here.

class CategoryManager(models.Manager):

    def new_category(self,category):
        new_category = self.create(category=re.sub('\s+','-',category).lower())
        new_category.save()
        return new_category

class Category(models.Model):

    category = models.CharField( verbose_name="Category", max_length = 250, blank = True, unique = True, null = True)

    # If we need to add Images in our Project we will need to install pillow.
    image = models.ImageField(upload_to = 'Images/Categories/', blank = True, null = True, verbose_name = "Image")

    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class Quiz(models.Model):
    ''' Quiz is onetomany modeled to Questions '''

    title = models.CharField(verbose_name= "Title", max_length = 50, blank = False)

    description = models.TextField(verbose_name = "Description", blank = True, help_text = "Quiz description")

    level = models.CharField(verbose_name = "Level", help_text = "Level of difficultly", max_length = 10,default = 'Easy',choices = (('Hard','Hard'),('Intermediate','Intermediate'),('Easy','Easy')))

    url = models.SlugField(max_length = 60, blank = False, help_text = "A user friendly url", verbose_name = "User Friendly Url")

    category = models.ForeignKey(Category, null = False, blank = True, verbose_name = "Category", on_delete = models.CASCADE)

    random_order = models.BooleanField(blank = False, default = True, verbose_name = "Random Order", help_text = "Display the questions in Random Order ?")

    max_questions = models.PositiveIntegerField(blank = False, null = False, default = 1, verbose_name = "Max_questions", help_text = "Number of questions to be displayed on each attempt")

    single_attempt = models.BooleanField(blank = False, default = False, help_text = "If selected, user will be allowed only one attempt for this quiz", verbose_name = "Single Attempt")

    pass_mark = models.PositiveSmallIntegerField(blank = True, default = 0, verbose_name = "Passing Marks", help_text = "Percentage required to pass", validators = [MaxValueValidator(100)])

    success_text = models.TextField(blank = True, help_text = "Displayed if user passes.", verbose_name = "Success Text")

    fail_text = models.TextField(blank = True, help_text = "Displayed if user fails", verbose_name = "Fail Text")

    draft = models.BooleanField(blank = True, default = False, verbose_name = "Draft", help_text = "Quiz won't be available to student if this is selected, only for internal assessment this quiz will be available")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        ''' overriding the default save because we need to slash the whitespaces in urls '''

        self.url = re.sub('\s+', '-', self.url).lower()
        self.url = ''.join(letter for letter in self.url if letter.isalnum() or letter == '-')

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    def total_marks(self):
        return sum(map(lambda x: x.marks,Question.objects.all().filter(quiz = self)))

    

class Question(models.Model):
    ''' Base class for all question types. Question properties are here '''

    quiz = models.ManyToManyField(Quiz, verbose_name = "Quiz", blank = True)

    category = models.ForeignKey(Category, verbose_name = "Category", blank = True, null = True, on_delete = models.CASCADE)

    # same as before, needs pillow
    figure = models.ImageField(upload_to='Images/Questions/', blank = True, null = True, verbose_name = "Question Image")

    content = models.CharField(max_length = 1000, blank = False, help_text = "Enter the Question (text)", verbose_name = 'Question')

    explanation = models.TextField(max_length = 2000, blank = True, help_text = "Explanation to be shown after the question is answered ", verbose_name = "Explanation")

    marks = models.PositiveSmallIntegerField(blank = False, default = 1, verbose_name = "Marks", help_text = "Marks alloted to this question", validators = [MaxValueValidator(50)] )


    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['category']

        def __str__(self):
            return self.content
    
    def get_marks(self):
        return self.marks

class Progress(models.Model):
    ''' Progress model is used to track users progress in particular quiz '''

    student = models.ForeignKey(User, null = False, blank = False, verbose_name = "Student", on_delete = models.CASCADE)

    quiz = models.ForeignKey(Quiz, null = False, blank = False, verbose_name = "Quiz", on_delete = models.CASCADE)

    attempted_on = models.DateTimeField(auto_now_add = True, verbose_name = "Attempted Quiz on ")

    Questions_attempted = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = "Question Attempted", default = 0)

    Questions_correct = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = "Questions Correctly answered", default = 0)

    marks = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = "Marks Scored", default = 0)

    class Meta:
        verbose_name = "Progress of Student"

        def __str__(self):
            return " - ".join([self.student.username, self.quiz.title])
