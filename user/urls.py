# urls.py
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from django.urls import path , include
from . import views
urlpatterns = [
    path('register/', RegisterView.as_view(
        serializer_class=CustomRegisterSerializer
    ), name='rest_register'),
    path('login/', views.CustomLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
     path('api/profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
]
