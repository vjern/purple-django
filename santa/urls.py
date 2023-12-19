from django.urls import path

from . import views

urlpatterns = [
    path("", views.liveness, name="index"),
    *views.router.urls,
]
