"""
    Models for timesheet entry.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from project_management.non_project_task.models import NonProjectTask
from project_management.tasks.models import Task
from project_management.projects.models import Project
from project_management.projects.models import ProjectSchedule
from django.http import HttpResponse
from datetime import datetime, timedelta


#from project_management.users.models import FiveGUser

class TaskTracking(models.Model):
    """
        Class representing the timesheet entry table.
    """
    user = models.ForeignKey(User)
    program = models.CharField(_('program'), max_length=40, blank=True,
                               null=True)
    task = models.CharField(_('task'), max_length=120, blank=True)
    is_program_task = models.BooleanField(_('program task status'),
                                          default=False)
    start_time = models.DateTimeField(_('start time'))
    time_spent = models.DecimalField(_('time spent'), max_digits=10,
                                     decimal_places=2)
    is_rework = models.BooleanField(_('rework'), default=False)

    class Meta:
        verbose_name = _('TaskTrackingEntry')
        verbose_name_plural = _('TaskTrackingEntries')

    def __unicode__(self):
        return "%s:%s" % (self.user, self.task)

    @classmethod
    def get_task(cls, task_id):
        """
            Returns the task for the specified id.
        """
        tasks = Task.objects.filter(id=task_id)
        if len(tasks) > 0:
            return tasks[0]
        return None

    @classmethod
    def get_project(cls, task_id):
        """
            Returns the project of the task and also whether it is a project based task.
        """
        task = cls.get_task(task_id)
        try:
            project = task.project.pk
        except BaseException:
            project = None
        return project, True if project else False

    @classmethod
    def get_projectname(cls, task_id):
        """
            Returns the project of the task and also whether it is a project based task.
        """
        task = cls.get_task(task_id)
        try:
            projectname = task.project.name
        except BaseException:
            projectname = None
        return projectname

    def save(self, **kwargs):
        """
            Overridden save method. Takes care of updates based on start_time.
        """
        WORK_HOURS = 8
        entries_to_update = TaskTracking.objects.filter(
            user=self.user).filter(start_time=self.start_time)
        if entries_to_update:
            for entry in entries_to_update:
                self.pk = entry.pk
        if self.program is not None:
            super(TaskTracking, self).save(**kwargs)
            total_time_spent = TaskTracking.objects.filter(
                program=self.program).aggregate(
                models.Sum('time_spent')).get('time_spent__sum')
            project = Project.objects.get(id=self.program)
            if(project.planned_effort):
                alloted_time = (project.planned_effort) * WORK_HOURS
                if(total_time_spent > alloted_time) and (project.estimated_time_exceed):
                    raise ProjTimeExceed(Exception)
            else:
                end_date = ProjectSchedule.objects.get(
                    id=self.program).planned_end_date
                today = datetime.now().date()
                if(today > end_date) and (project.estimated_time_exceed):
                    raise ProjTimeExceed(Exception)
        super(TaskTracking, self).save(**kwargs)

    def delete(self):
        super(TaskTracking, self).delete()


class ProjTimeExceed(Exception):
    pass
