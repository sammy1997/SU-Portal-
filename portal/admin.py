from django.contrib import admin
from models import Cost, Bus
# Register your models here.


class CostAdmin(admin.ModelAdmin):
    search_fields = ['name', 'institute_id']


admin.site.register(Cost, CostAdmin)
admin.site.register(Bus)
