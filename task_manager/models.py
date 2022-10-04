from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    cat_field = models.TextField()

