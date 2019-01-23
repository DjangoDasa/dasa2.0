from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from .views import home_view, index, RegisterApiView, UserApiView, AnalysisApiView


urlpatterns = [
    path('', home_view, name='home'),
    path('user/<int:pk>', UserApiView.as_view(), name='user-detail'),
    path('register', RegisterApiView.as_view(), name='register'),
    path('login', views.obtain_auth_token),
    path('analysis', AnalysisApiView.as_view(), name='analysis-list'),

]


