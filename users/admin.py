from django.contrib import admin
from .models import Profile
from .models import Notification
from .models import SocialLink


# Register/Customize your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_pic", "status")
    list_filter = ["status"]
    search_fields = [
        "user",
    ]
    ordering = ["status"]
    actions = ["make_user_online", "make_user_offline"]

    # Hide a question
    @admin.action(description="Make selected users offline")
    def make_user_offline(modeladmin, request, queryset):
        queryset.update(status="False")

    # Publish question
    @admin.action(description="Make selected users online")
    def make_user_online(modeladmin, request, queryset):
        queryset.update(status="True")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """docstring for SocialLinkAdmin"""

    list_display = ("profile", "link")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """docstring for NotificationAdmin"""

    list_display = ("notifier",)
