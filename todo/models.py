from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    resolved = models.BooleanField(default=False)
    # New: optional due date
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title