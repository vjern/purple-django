from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("draw", views.new_draw, name="new_draw"),
    *views.urlpatterns,
]
