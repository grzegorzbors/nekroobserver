from django.contrib import admin

# Register your models here.
from .models import Profiles,  Keywords

# Register your models here.
#to umożliwia edycję w panelu admina
admin.site.register(Profiles)
admin.site.register(Keywords)