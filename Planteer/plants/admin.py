from django.contrib import admin
from .models import Benefit, Comment , Contact, Countries, Plant


class PlanteerAdmin(admin.ModelAdmin):
    list_display = ("name","created_at")
    list_filter = ("plant",)
    

admin.site.register(Comment, PlanteerAdmin)
admin.site.register(Contact)
admin.site.register(Benefit)
admin.site.register(Plant)   
admin.site.register(Countries)




