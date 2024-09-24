from django.db import models
from django.contrib.auth.models import User
import json


class Notification(models.Model):
    message = models.CharField(max_length=255)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.message


class TokenTracker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Token count for {self.user.username}"


class PdfChat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default=None)
    vector_database = models.JSONField()
    answer_array = models.TextField()

    def set_vector_database(self, obj):
        self.vector_database = json.dumps(obj)

    def get_vector_database(self):
        return json.loads(self.vector_database)

    def set_answer_array(self, answer_array):
        self.answer_array = json.dumps(self.answer_array)

    def get_answer_array(self):
        return json.loads(self.answer_array)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.TextField()
    message = models.TextField(default=None)

    def __str__(self):
        return self.email
