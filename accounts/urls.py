from django.urls import path
from accounts import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change_password/',PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/profile/'),name='change_password'),
]