from django.urls import path

from . import views

urlpatterns = [
    path('facebook/', views.FacebookSocialAuthView.as_view()),
    path('google/', views.GoogleSocialAuthView.as_view()),
]
