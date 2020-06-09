from django.contrib import admin

# Register your models here.

from twitter.models import Tweet, Comment, Message

#admin.site.register(Tweet)
#admin.site.register(Comment)
#admin.site.register(Message)

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("content", "creation_date")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "user")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message", "to", "sender")