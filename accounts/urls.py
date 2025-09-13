from django.urls import path
from . import views

urlpatterns = [
   path('', views.dashboard, name='dashboard'),
   path('dashboard/', views.dashboard, name='dashboard'),

   path('register/', views.register, name='register'),
   path('login/', views.loginn, name='login'),
   path('logout/', views.logoutt, name='logout'),
   path('activate/<uidb64>/<token>/', views.activate, name='activate'),

   path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
   path('resetPassword/<uidb64>/<token>/', views.resetPassword, name='resetPassword'),

]