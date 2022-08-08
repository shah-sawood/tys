from django.contrib import admin
from tests.models import File

# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_filter = ("category",)
    list_display = ("file", "category")
