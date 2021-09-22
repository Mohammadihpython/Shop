from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Products
from .serializer import CommentSerializer
from ..models import Comment


class CommentApiView(generics.GenericAPIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwarg):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            product_id = serializer.data.get('product_id')
            text = serializer.data.get('text')
            rate = serializer.data.get('rate')
            reply_id = serializer.data.get('reply')
            reply = serializer.data.get('reply')
            comment_id = serializer.data.get('comment_id')
            try:
                product = Products.objects.get(id=product_id)
                if reply:
                    Comment.objects.create(
                        user_od=user.id,
                        product_id=product.id,
                        rate=rate,
                        text=text,
                        reply_id=comment_id,
                        is_reply=True,
                    )
                    return Response(status=status.HTTP_201_CREATED, data='comment create')
                else:
                    Comment.objects.create(
                        user_od=user.id,
                        product_id=product.id,
                        text=text,
                        is_reply=False,
                    )
                    return Response(status=status.HTTP_201_CREATED, data='reply add to comment')
            except Products.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='queryset does not matching')


class CommentListApiView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        query = Comment.objects.filter(product_id=product_id)
        return query