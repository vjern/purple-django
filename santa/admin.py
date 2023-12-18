from django.contrib import admin

# Register your models here.
from .models import User, Exclusion

for model in User, Exclusion:
    admin.site.register(model)
