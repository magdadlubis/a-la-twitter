from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserModel = get_user_model()

class Tweet(models.Model):
    content = models.CharField(max_length=140, verbose_name='Wpis')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Data wpisu')
    user = models.ForeignKey(UserModel, verbose_name='Użytkownik', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Comment(models.Model):
    comment = models.CharField(max_length=60, verbose_name='Komentarz')
    user = models.ForeignKey(UserModel, verbose_name='Użytkownik', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, verbose_name='Wpis', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Message(models.Model):
    message = models.TextField(verbose_name='Wiadomość')
    to = models.ForeignKey(UserModel, verbose_name='Odbiorca', on_delete=models.CASCADE, related_name='received')
    sender = models.ForeignKey(UserModel, verbose_name='Nadawca', on_delete=models.CASCADE, related_name='sent')
    read = models.BooleanField(default=False, verbose_name='Przeczytana')
    date = models.DateTimeField(verbose_name='Data wysłania', auto_now_add=True, null=True)

    def __str__(self):
        return self.message