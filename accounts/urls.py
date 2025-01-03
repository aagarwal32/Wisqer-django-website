from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('register', views.register_user, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name='logout'),
    path('profile/<int:pk>/', views.AccountPageView.as_view(), name="user_account"),
    path('user/delete/', views.AccountDeleteView.as_view(), name="user_account_delete"),
]