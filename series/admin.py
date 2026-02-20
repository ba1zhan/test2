from django.contrib import admin
from series.models import Category, Series, Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)



@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name",  "category", "created_at", "updated_at")
    list_filter = ("category",)