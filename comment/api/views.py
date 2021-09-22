from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Products
from .serializer import CommentSerializer, ReplySerializer
from ..models import Comment


class CommentApiView(generics.GenericAPIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwarg):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            product_id = serializer.data.get('product')
            text = serializer.data.get('text')
            rate = serializer.data.get('rate')
            # reply_id = serializer.data.get('reply')
            reply = serializer.data.get('reply')
            comment_id = serializer.data.get('comment_id')
            try:
                product = Products.objects.get(id=product_id)
                Comment.objects.create(
                    user_id=user.id,
                    product_id=product.id,
                    text=text,
                    is_reply=False,
                )
                return Response(status=status.HTTP_201_CREATED, data='your comment add to comments')
            except Products.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='queryset does not matching')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )


class ReplyCommentApiView(generics.GenericAPIView):
    serializer_class = ReplySerializer

    def post(self, request, *args, **kwarg):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            product_id = serializer.data.get('product')
            text = serializer.data.get('text')
            rate = serializer.data.get('rate')
            reply_id = serializer.data.get('reply')
            comment_id = serializer.data.get('comment_id')
            try:
                product = Products.objects.get(id=product_id)
                comment = Comment.objects.get(id=reply_id)
                Comment.objects.create(
                    user_id=user.id,
                    product_id=product.id,
                    rate=rate,
                    text=text,
                    reply_id=comment.id,
                    is_reply=True,
                )
                return Response(status=status.HTTP_201_CREATED, data='reply add :)')

            except Products.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='queryset does not matching')

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )


class CommentListApiView(generics.ListAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        query = Comment.objects.filter(product_id=product_id)
        return query
