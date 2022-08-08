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


# add new question
@login_required
def add_question(request, category_id=None):

    category_id = category_id if category_id else ""
    categories = (
        Category.objects.filter(pk__exact=category_id)
        if category_id
        else Category.objects.all()
    )
    context = {
        "title": "Add Question",
        "categories": categories,
    }

    # when method is post
    if request.method == "POST":
        # populate forms with posted data
        q_form = QuestionForm(request.POST)
        choice_1 = request.POST.get("choice_1")
        choice_2 = request.POST.get("choice_2")
        choice_3 = request.POST.get("choice_3")
        choice_4 = request.POST.get("choice_4")
        correct_choice = int(request.POST.get("correct_choice"))
        category_id = request.POST.get("category")

        # validate posted data
        if (
            q_form.is_valid()
            and choice_1
            and choice_2
            and choice_3
            and choice_4
            and category_id
        ):
            category = Category.objects.get(id=category_id)

            question = q_form.save(commit=False)
            question.category = category  # add category to question
            question.save()  # save question

            choices = [
                Choice.objects.create(option=choice_1, question=question),
                Choice.objects.create(option=choice_2, question=question),
                Choice.objects.create(option=choice_3, question=question),
                Choice.objects.create(option=choice_4, question=question),
            ]
            choice = Choice.objects.get(id=choices[correct_choice].id)
            choice.correct = True
            choice.save()
            messages.success(request, "Question added successfully.")
        else:
            context["errors"] = q_form.errors
        return HttpResponseRedirect(reverse("tests:take-a-test", args=[category_id]))

    # when method is not post
    return render(request, "tests/add/question.html", context)
