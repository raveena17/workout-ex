from datetime import datetime
from django.core.management.base import BaseCommand
from project_management.projects.views import *
from project_management.projectbudget.views import budget_reminder_alertmail


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "cron run at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ext_appr_cron(self)
        budget_reminder_alertmail(self)
