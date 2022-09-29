from django import forms

from .models import Category
from .models import Choice
from .models import Question
from .models import File


# Question Form
class QuestionForm(forms.ModelForm):
    """question form"""

    class Meta:
        model = Question
        fields = ["statement", "published"]


# Category Form
class CategoryForm(forms.ModelForm):
    """add/update category form"""

    class Meta:
        model = Category
        fields = "__all__"


class ChoiceForm(forms.ModelForm):
    """choice form"""

    class Meta:
        model = Choice
        fields = ["option"]


class FileForm(forms.ModelForm):
    """file form"""

    class Meta:
        model = File
        fields = "__all__"
