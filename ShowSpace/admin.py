from django.contrib import admin

from .models import isilon
from .models import radar05
from .models import radar05_details


# Register your models here.

class isilon_help(admin.ModelAdmin):
    list_display = ('folder_name', 'scan_date', 'total_space', 'used_space', 'used_space', 'percentage')
    list_filter = ('scan_date',)


class radar05_help(admin.ModelAdmin):
    list_display = ('folder_name', 'folder_size', 'scan_date')
    list_filter = ('scan_date', 'folder_name')


class radar05_details_help(admin.ModelAdmin):
    list_display = ('folder_name', 'type', 'size', 'scan_date')
    list_filter = ('type', 'scan_date')


admin.site.register(isilon, isilon_help)
admin.site.register(radar05, radar05_help)
admin.site.register(radar05_details, radar05_details_help)
