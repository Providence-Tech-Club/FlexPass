from django.contrib import admin

# Register your models here.
from .models import Classroom, Request

admin.site.register(Classroom)
admin.site.register(Request)
