from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from .models import Comment


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','text','rate','reply','create','is_reply']
