from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from .models import CommentForm, Comment


def Product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(user_id=request.user.id, text=data['text'], rate=data['rate'], product_id=id)
            messages.success(request, 'add comment :)')
        return redirect(url)
