from django.db import models

# Create your models here.
class Feedback(models.Model):
    feedback_date = models.DateTimeField()
    feedbackers_name = models.CharField(max_length=100)
    feedbackers_email = models.EmailField()
    feedback_message = models.TextField()
    