from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from .views import home_view, index, RegisterApiView, UserApiView
from .views import AnalysisApiView, AnalysisGraphApiView, UsersAllApiView


urlpatterns = [
    path('', index, name='home'),
    path('user/<int:pk>', UserApiView.as_view(), name='user-detail'),
    path('users', UsersAllApiView.as_view(), name='users-all'),
    path('register', RegisterApiView.as_view(), name='register'),
    path('login', views.obtain_auth_token),
    path('analysis', AnalysisApiView.as_view(), name='analysis-list'),
    path('chart', AnalysisGraphApiView.as_view(), name='analysis-graph')
    # path('analysis/<chart>', AnalysisGraphApiView.as_view(), name='analysis-graph'),
#     path('charts/{graph_type}', ChartApiView.as_view(), name='chart-detail'),

]


