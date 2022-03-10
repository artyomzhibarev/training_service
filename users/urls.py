from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.CreateCustomerAPIView.as_view(), name='create_user'),
    path('login/', obtain_auth_token, name='login_user'),
    path('logout/', views.LogoutCustomerAPIView.as_view(), name='logout_user'),
]
