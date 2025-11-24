from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.plant_list, name="plant_list"),
    path("new/", views.plant_create, name="plant_create"),
    path("<int:plant_id>/", views.plant_detail, name="plant_detail"),
    path("<int:plant_id>/update/", views.plant_update, name="plant_update"),
    path("<int:plant_id>/delete/", views.plant_delete, name="plant_delete"),
    path("search/", views.plant_search, name="plant_search"),
    path("contact/", views.contact_view, name="contact"),
    path("contact/messages/", views.contact_messages_view, name="contact_messages"),
    path("country/<int:country_id>/", views.plants_by_country, name="plants_by_country"),
]
