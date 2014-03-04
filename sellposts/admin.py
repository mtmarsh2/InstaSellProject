from django.contrib import admin
from .models import SellPost 

class SellPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(SellPost, SellPostAdmin)
