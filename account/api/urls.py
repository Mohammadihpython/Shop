from django.urls import path
from .views import LoginApiView,SignUpApiView,ChangePasswordUpdate
app_name = 'apiAccount'
urlpatterns = [
    # user Apis
    path('register/', SignUpApiView.as_view(), name='api_register'),
    path('login/',LoginApiView .as_view(), name='api_login'),
    path('changepaswd/',ChangePasswordUpdate .as_view(), name='api_update_password'),
]
