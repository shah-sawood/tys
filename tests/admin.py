from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

# Register your models here.

# customizing question on admin site
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("statement", "published", "date_updated")
    list_filter = ("published",)
    search_fields = [
        "statement",
    ]
    ordering = ["statement"]
    actions = ["publish_question", "hide_question"]
    date_hierarchy = "date_updated"

    # Hide a question
    @admin.action(description="Hide selected questions")
    def hide_question(modeladmin, request, queryset):
        queryset.update(published="False")

    # Publish question
    @admin.action(description="Publish selected questions")
    def publish_question(modeladmin, request, queryset):
        queryset.update(published="True")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = [
        "date_updated",
    ]


@admin.register(models.Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_filter = ["question", "correct"]
    search_fields = ["option"]
