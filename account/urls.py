from . import views
from django.urls import path

urlpatterns = [
    path('login', views.login_view),
    path('signup', views.register_view),
    path('refresh-token', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
]
