"""
    Model for Task
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from project_management.projects.models import Project
from project_management.milestone.models import Milestone

import mptt
import datetime


class Type(models.Model):
    """
       Representing task type model for the task.
    """
    name = models.CharField(_('name'), max_length=120)
    is_project_type = models.BooleanField(_('is_project_type'), default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class SubType(models.Model):
    """
        Representing task sub type for the task
    """
    name = models.CharField(_('name'), max_length=120)
    type = models.ForeignKey(Type, verbose_name=_('type'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('SubType')
        verbose_name_plural = ('SubTypes')


class AbstractTask(models.Model):
    """
        Abstract class for the Task
    """
    PRIORITY_CHOICES = (
        ('blocker', _('blocker')),
        ('critical', _('critical')),
        ('major', _('major')),
        ('minor', _('minor')),
        ('trivial', _('trivial'))
    )
    STATUS_CHOICES = (
        ('open', _('open')),
        ('closed', _('closed')),
        ('hold', _('hold')),
        ('Unreviewed', _('Unreviewed')),
        ('Design decision needed', _('Design decision needed')),
        ('Accepted', _('Accepted')),
        ('Ready for checkin', _('Ready for checkin')),
        ('Fixed on a branch', _('Fixed on a branch'))
    )
    name = models.CharField(_('Task Name'), max_length=120)
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'),
                                      default=datetime.datetime.now, editable=False)
    author = models.ForeignKey(User, verbose_name=_('author'),
                               related_name='created_%(class)s', blank=True)
    assigned_resources = models.ManyToManyField(User,
                                                verbose_name=_('Assigned Resources'))
    status = models.CharField(choices=STATUS_CHOICES, null=True,
                              max_length=120)
    priority = models.CharField(choices=PRIORITY_CHOICES, null=True,
                                max_length=120)
    editor = models.ForeignKey(User, verbose_name=_('editor'),
                               related_name="%(app_label)s_%(class)s_user", blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'),
                              related_name='owned_%(class)s')
    notes = models.TextField(_('Description'), null=True, blank=True)

    class Meta:
        abstract = True


class Task(AbstractTask):
    """
        Representing task model.
    """

    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        verbose_name=_('project'))
    type = models.ForeignKey(Type, verbose_name=_('Task Type'))
    sub_type = models.ForeignKey(SubType, verbose_name=_('Task Sub Type'),
                                 blank=True, null=True)
    milestone = models.ForeignKey(Milestone, verbose_name=_('milestone'),
                                  null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="%(app_label)s_%(class)s_parent", verbose_name=_('Module'))
    share_to_all = models.BooleanField(_('Share Task'), default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']


mptt.register(Task, order_insertion_by=['name'])
