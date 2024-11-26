from django.urls import path
from .views import sign_up_user, log_in_user, log_out_user

urlpatterns = [
    path('signup/', sign_up_user, name='signup'),
    path('login/', log_in_user, name='login'),
    path('logout/', log_out_user, name='logout'),
]