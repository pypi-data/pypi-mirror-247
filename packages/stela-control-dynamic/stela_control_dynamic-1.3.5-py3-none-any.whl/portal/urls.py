from django.urls import path, include
from . import views
  
app_name="portal"

urlpatterns = [
    #stela Home
    path('i18n/', include('django.conf.urls.i18n')),
    path('auth/login/', views.login, name="login"),
    path('auth/register/', views.account_register, name="register"),
    path('auth/logout/', views.logout, name="logout"),
    
 ]   