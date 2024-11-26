from django.urls import path
from .views import user_profile, get_user_profile

urlpatterns = [
    path('api/v1/profile/', user_profile, name='profile'),
    path('api/v1/profile/<int:user_id>/', get_user_profile, name='get_user_profile'),
]
