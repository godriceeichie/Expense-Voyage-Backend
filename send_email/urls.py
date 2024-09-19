from django.urls import path
from . import views

urlpatterns = [
    path("reset-password-link", views.password_reset_link_email),
]
