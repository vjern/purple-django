from django.contrib import admin

# Register your models here.
from .models import User, Ban

for model in User, Ban:
    admin.site.register(model)
