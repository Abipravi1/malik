from django.contrib import admin

# Register your models here.
from .models import *

data = [Tokens]

for x in data:
    admin.site.register(x)