"""all backend goes here"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


from users.models import Profile
from users.models import SocialLink
from users.models import Notification
from .forms import QuestionForm
from .forms import ChoiceForm
from .forms import CategoryForm

from .models import Category
from .models import Choice
from .models import Question

from .decorators import is_admin

G = ["GET"]
P = ["POST"]
B = ["GET", "POST"]


@login_required
@require_http_methods(G)
def categories(request):

    categories = Category.objects.filter().order_by("-date_updated")
    context = {
        "title": f"Categories || {categories.count()}",
        "categories": categories,
    }
    return render(request, "tests/category.html", context)


# detail page
@require_http_methods(G)
@login_required
def show_questions(request, category_id):
    """display all questions related to requested category"""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))

    context = {
        "title": f"Category - {category} ({category.get_num_of_questions()})",
        "category": category,
    }
    return render(request, "tests/detail.html", context)
