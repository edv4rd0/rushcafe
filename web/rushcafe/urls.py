from django.contrib.auth import views as auth_views
from django.urls import path

from rushcafe import views
from rushcafe.forms import RushCafeAuthForm

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='login.html',
             redirect_field_name='index',
             authentication_form=RushCafeAuthForm
         ), name='login'),
]
