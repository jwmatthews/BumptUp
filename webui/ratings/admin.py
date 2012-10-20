from django.contrib import admin
from ratings.models import Category, Rating

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {"fields": ["owner", "title", "description", "display"]}),
        ("Date information",    {"fields": ["created", "modified"]})
    ]
    list_display = ("owner", "title", "description", "display", "created", "modified")
    list_filter = ["display", "created", "modified"]
    search_fields = ["title", "description"]
    date_hierachy = "created"

class RatingAdmin(admin.ModelAdmin):
    fields = ["category", "score", "rater", "created"]
    list_display = ("category", "rater", "score", "created")
    list_filter = ["score", "created"]
    search_fields=["category"]
    date_hierachy = "created"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating, RatingAdmin)