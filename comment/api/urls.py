from django.urls import path
from .views import CommentListApiView, CommentApiView

app_name = 'apiComment'
urlpatterns = [
    path('create/', CommentApiView.as_view(), name='create_comment_reply'),
    path('list/', CommentListApiView.as_view(), name='list-comment'),

]
