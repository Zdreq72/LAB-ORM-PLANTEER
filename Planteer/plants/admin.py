from django.contrib import admin
from .models import Comment , Contact


class PlanteerAdmin(admin.ModelAdmin):
    list_display = ("name","created_at")
    list_filter = ("plant",)

admin.site.register(Comment, PlanteerAdmin)
admin.site.register(Contact)





