"""tests URL Configuration

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

"""
name of the application
prepend url name by application name to avoid namespacing
"""
app_name = "tests"

# category urls
category = [
    path("", views.categories, name="categories"),
    path("<category_id>/", views.show_questions, name="take-a-test"),
]

# add urls
add = [
    path("question/", views.add_question, name="add-question"),
    path("question/<category_id>/", views.add_question, name="add-question"),
]

# overall urls
urlpatterns = [
    path("category/", include(category)),
    path("add/", include(add)),
]
