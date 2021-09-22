from rest_framework import serializers
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'user',
            'product',
            'text',
            'rate',
        )


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'user',
            'product',
            'text',
            'rate',
            'reply',
        )
