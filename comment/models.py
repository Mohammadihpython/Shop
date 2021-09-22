from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from product.models import Products

User = get_user_model()


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    text = models.TextField(verbose_name=_('text'), )
    rate = models.PositiveIntegerField(default=1)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reply')
    create = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        name = [str(self.user), str(self.product)]
        return '__'.join(name)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]