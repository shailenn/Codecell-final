from django.db import models
from Quiz.models import Question

ANSWER_ORDER_OPTIONS = (
    ('content','Content'),
    ('random','Random')
)

class MCQ(Question):

    answer_order = models.CharField(max_length = 30, choices = ANSWER_ORDER_OPTIONS, help_text = "The order in which the answer options are to be displayed", verbose_name = "Answer Options Order")

    single_correct = models.BooleanField(default = True, help_text = "If selected, only one choice should have a correct answer", verbose_name = "Single Correct")
    
    class Meta:
        verbose_name = "Multiple Choice Question"


class Answer(models.Model):

    question = models.ForeignKey(MCQ, verbose_name = "Question", on_delete = models.CASCADE)

    content = models.CharField(max_length = 1000, blank = False, help_text = "Enter the answer text to be displayed",verbose_name = "Answer text")

    correct = models.BooleanField(blank = False, default = False, help_text = "Is this a correct Answer ?", verbose_name = "Correct")

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.content