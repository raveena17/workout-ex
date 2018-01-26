from django.contrib import admin

from .models import ClientVisitReport


class cvrList_admin(admin.ModelAdmin):
    list_display = ['prepared_by', 'project_name', 'client_name', 'visit_location',
                    'date_of_visit']



admin.site.register(ClientVisitReport, cvrList_admin)


