from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Note,Label,Img
# Register your models here.

admin.site.register(Note)
admin.site.register(Label)
admin.site.register(Img)