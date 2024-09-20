from . import views
from django.urls import path

urlpatterns = [
    path('login', views.login_view),
    path('signup', views.register_view),
    path('refresh-token', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
    path("reset-password/<str:token>", views.reset_password_view),
    path('user', views.user_view),
    path('user/<int:user_id>', views.delete_user_view)
]
