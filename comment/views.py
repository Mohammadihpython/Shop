from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from .models import CommentForm, Comment, ReplyForm


def Product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(user_id=request.user.id, text=data['text'], rate=data['rate'], product_id=id)
            messages.success(request, 'add comment :)')
        return redirect(url)


def product_reply(request, id, comment_id):
    if request.method == 'POSt':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'], product_id=id
                                   , user_id=request.user.id,
                                   reply_id=comment_id,
                                   is_reply=True
                                   )
