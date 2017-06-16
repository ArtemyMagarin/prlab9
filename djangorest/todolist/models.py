from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework.authtoken.models import Token

def token_request(request):
    if user_requested_token() and token_request_is_warranted():
        new_token = Token.objects.create(user=request.user)


class User(User):
    username_validator = ASCIIUsernameValidator()

    class Meta:
        proxy = True  # If no new field is added.
        
    def __str__(self):
        return "{}".format(self.firstname + " " + self.surname)

class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE) 


    def __str__(self):
        return "{}".format(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)

    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')
    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tag_id')

    def __str__(self):
        return "{}".format(self.name + " " + self.description)
