from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


from tests.decorators import is_admin
from tests.forms import QuestionForm, CategoryForm, FileForm
from tests.models import Category, Choice, Question
from users.forms import RegistrationForm
from users.models import Notification

from .helpers import add_questions_to_db


# Create your views here.
@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def index(request):
    context = {
        "title": "Index",
    }
    return render(request, "superuser/index.html", context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def show_categories(request):
    categories = Category.objects.all().order_by("-id")
    context = {
        "title": "Categories . {}".format(categories.count()),
        "categories": categories,
    }
    return render(request, "superuser/categories.html", context)


@login_required
@user_passes_test(is_admin)
def show_category(request, category_id):
    try:
        category = Category.objects.get(pk__exact=category_id)
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse("superuser:index"))
    context = {
        "title": "Category - {}".format(category.get_num_of_questions()),
        "category": category,
    }
    return render(request, "superuser/category.html", context)


# add category
@user_passes_test(is_admin)
@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
        else:
            messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(reverse("superuser:categories"))
    context = {"title": "Add Category"}
    return render(request, "superuser/add/category.html", context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_category(request):
    category_id = request.POST.get("id")
    try:
        category = Category.objects.get(id=category_id).delete()
        messages.success(request, "Category deleted successfully.")
    except Category.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
    return HttpResponseRedirect(reverse("superuser:categories"))


# edit category
@user_passes_test(is_admin)
@login_required
def edit_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "The requested category does not exist.")
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return HttpResponseRedirect(
                reverse("superuser:category", args=[category_id])
            )
        else:
            messages.error(request, "Something went wrong. Please try again later.")
    else:
        context = {
            "title": "Update - {}".format(category.get_name()),
            "category": category,
        }
        return render(request, "superuser/update/category.html", context)
    return HttpResponseRedirect(reverse("superuser:categories"))


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
            if request.user.is_superuser:
                question.published = True
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
            messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(reverse("superuser:category", args=[category_id]))

    # when method is not post
    return render(request, "superuser/add/question.html", context)


@login_required
@require_http_methods(["GET"])
@user_passes_test(is_admin)
def show_questions(request):
    context = {"title": "Questions", "questions": Question.objects.all()}
    return render(request, "superuser/questions.html", context)


# upload questions file
@login_required
@user_passes_test(is_admin)
def upload_questions(request):
    """add questions from uploaded file"""
    context = {"title": "Upload questions file", "categories": Category.objects.all()}
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            category = obj.category
            filename = obj.file.url[1:]
            counter = add_questions_to_db(filename, category)
            messages.success(request, f"{counter} questions added successfully.")
            return HttpResponseRedirect(
                reverse("superuser:category", args=[category.get_id()])
            )
        else:
            messages.error(request, "Something went wrong. Please try again later.")
            return HttpResponseRedirect(reverse("superuser:categories"))
    return render(request, "superuser/add/questions.html", context)


# delete a question
@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_question(request):
    # try to get request question for deletion
    question_id = request.POST.get("question_id")
    try:
        question = Question.objects.get(id=question_id)
        category_id = question.category.id
    except Question.DoesNotExist:
        messages.error(
            request,
            "Something went wrong. Please try again later.",
        )
    else:
        question.delete()  # delete quesiton
        messages.success(request, "Question deleted successfully.")
    finally:
        return HttpResponseRedirect(reverse("superuser:show-questions"))


@login_required
@user_passes_test(is_admin)
def edit_question(request, question_id):
    context = {"title": "Update question"}
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(reverse("superuser:show-questions"))
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            q = form.save(commit=False)
            q.published = True
            q.save()
            messages.success(request, "Question updated successfully.")
            return HttpResponseRedirect(
                reverse(
                    "superuser:category", args=[question.get_category().get_id()]
                )
            )
        else:
            messages.error(request, "Something went wrong during form validation.")

    context["question"] = question
    return render(request, "superuser/update/question.html", context)


# add choice to requested question
@login_required
@user_passes_test(is_admin)
def add_choice(request, question_id):
    """add choice to requested question"""
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))

    choice = request.POST.get("choice1")
    Choice.objects.create(option=choice, question=question)

    return HttpResponseRedirect(reverse("tests:questions", args=[question.category.id]))


@user_passes_test(is_admin)
@login_required
def approve_question(request):
    """approve question"""
    question_id = request.GET.get("question_id")
    notification_id = request.GET.get("notification_id")
    print("{ question_id = }")
    print("{ notification_id = }")
    try:
        question = Question.objects.get(pk=question_id)
        question.published = True
        question.save()

        notificaiton = Notification.notifications.get(pk=notification_id)
        notificaiton.is_read = True
        notificaiton.save()
    except (Question.DoesNotExist, Notification.DoesNotExist):
        messages.error(request, 'The system encountered a problem. Please try again later.')
    else:
        messages.success(request, "Question approved successfully.")
    finally:
        return HttpResponseRedirect(reverse("superuser:index"))


@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(is_admin)
def add_user(request):
    context = {
        "title": "Add User",
    }
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.cleaned_data["password"] == request.POST.get(
            "confirm_password"
        ):
            user = form.save(commit=False)
            user.email = user.username
            user.save()
            messages.success(request, "user created successfully.")
            return HttpResponseRedirect(reverse("superuser:profile", args=[user.id]))
        else:
            messages.error(request, "Please confirm password.")
            context["username"] = form.cleaned_data["username"]
            context["first_name"] = form.cleaned_data["first_name"]
            context["last_name"] = form.cleaned_data["last_name"]
    return render(request, "superuser/add/user.html", context)


@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(is_admin)
def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
    context = {"title": "Profile {}".format(user.get_username()), "user": user}
    return render(request, "superuser/profile.html", context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def update_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = request.user
    return render(
        request,
        "superuser/update/profile.html",
        {
            "title": f"Settings - {user.get_username()}",
            "user": user,
        },
    )


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def users(request):
    users = User.objects.filter(is_superuser=False)
    context = {
        "title": "Users - {}".format(users.count()),
        "users": users,
    }
    return render(request, "superuser/users.html", context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def authorize_as_admin(request):
    user_id = request.GET.get("user_id")
    group_name = request.GET.get("group_name")
    try:
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)
    except (User.DoesNotExist, Group.DoesNotExist):
        messages.error(request, "Our system encountered a problem. Please try again later.")
    else:
        if user.groups.filter(name=group_name).exists():
            user.groups.remove(group)
            if not user.groups.filter().exists():
                user.is_staff = False
            user.save()
            messages.success(
                request, "{} is no longer {}.".format(user.get_username(), group_name)
            )
        else:
            user.is_staff = True
            user.groups.add(group)
            user.save()
            messages.success(request, "{} is {} now.".format(user.get_username(), group_name))
    finally:
        return HttpResponseRedirect(reverse("superuser:users"))


def show_notifications(request):
    context = {
        "title": "notifications",
        "notifications": Notification.notifications.filter(is_read=False),
    }
    return render(request, "superuser/notifications.html", context)
