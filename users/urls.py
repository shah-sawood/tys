"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from . import views

# application name
app_name = "users"

update = [
    path("<int:user_id>bio/", views.update_bio, name="update-bio"),
    path(
        "<int:user_id>personal/info/",
        views.update_personal_info,
        name="update-personal-info",
    ),
    path("profile/", views.update_profile, name="update-profile"),
    path(
        "<int:user_id>/profile/picture/",
        views.update_profile_picture,
        name="update-profile-picture",
    ),
]

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("user/<user_id>/", views.profile, name="profile"),
    path("update/", include(update)),
]
