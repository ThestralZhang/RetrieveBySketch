from django.contrib import admin
from .models import Image
from .models import LikeInfo

# Register your models here.
admin.site.register(Image)
admin.site.register(LikeInfo)
