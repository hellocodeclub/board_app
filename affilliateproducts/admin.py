from django.contrib import admin
from .models import AffilliateProduct

# Register your models here.

class AffilliateProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','clicked_count')
    # list_display_links = ('id','title'),

admin.site.register(AffilliateProduct, AffilliateProductAdmin)
