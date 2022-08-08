"""superuser URL Configuration

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

app_name = "superuser"

# add urls
add = [
    path("category/", views.add_category, name="add-category"),
    path("question/", views.add_question, name="add-question"),
    path("question/<int:category_id>/", views.add_question, name="add-question"),
    path("questions/", views.upload_questions, name="upload-questions"),
    path("choice/<question_id>/", views.add_choice, name="add-choice"),
    path("user/", views.add_user, name="add-user"),
]

# category urls
category = [
    path("", views.show_categories, name="categories"),
    path("<category_id>/", views.show_category, name="category"),
]

# delete urls
delete = [
    path("question/", views.delete_question, name="delete-question"),
    path("category/", views.delete_category, name="delete-category"),
]

# edit urls
edit = [
    path("category/<category_id>/", views.edit_category, name="edit-category"),
    path("question/<question_id>/", views.edit_question, name="edit-question"),
]

# user urls
user = [
    path("", views.users, name="users"),
    path("authorize-as-admin/", views.authorize_as_admin, name="authorize-as-admin"),
    path("<user_id>/", views.profile, name="profile"),
    path("<user_id>/update/profile", views.update_profile, name="update-profile"),
]


urlpatterns = [
    path("", views.index, name="index"),
    path("category/", include(category)),
    path("add/", include(add)),
    path("delete/", include(delete)),
    path("edit/", include(edit)),
    path("user/", include(user)),
    path("questions/", views.show_questions, name="show-questions"),
    path("approve/question/", views.approve_question, name="approve-question"),
]
