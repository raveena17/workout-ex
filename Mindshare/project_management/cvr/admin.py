# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Cvr

class cvrList_admin(admin.ModelAdmin):
    list_display = ['prepared_by', 'project_name', 'client_name', 'visit_location',
                    'date_of_visit', 'approved_by', 'date_of_approval']

admin.site.register(Cvr, cvrList_admin)
# Register your models here.
