from django.urls import path
from .import views

urlpatterns = [
    path('test-cookie/', views.test_cookie),
    path('test-session/', views.test_session),
    path('random-string/', views.random_string),
]