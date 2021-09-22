from django.urls import path
from .views import CommentListApiView, CommentApiView,ReplyCommentApiView

app_name = 'apiComment'
urlpatterns = [
    path('create/', CommentApiView.as_view(), name='create_comment_reply'),
    path('reply/', ReplyCommentApiView.as_view(), name='create_reply'),
    path('list/<int:product_id>/', CommentListApiView.as_view(), name='list-comment'),

]
