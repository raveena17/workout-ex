from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from project_management.projectbudget.tests.logintest import LoginTest
from project_management.business_unit.models import BusinessUnit
from project_management.projects.models import ProjectSchedule, Project
from project_management.projects.models import ProjectMembership
from project_management.code_review.models import CodeReview
from project_management.projectbudget.tests.viewstest import create_project


class CodereviewTest(TestCase):
    cleint = Client()

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

        '''
        create project
        '''
        create_project()
        self.user_list = User.objects.all()
        self.project = Project.objects.all()[0].id

        '''
        Add team to the proeject
        '''
        ProjectMembership(project=Project.objects.all()[0],
                          member=self.user_list[0]).save()
        ProjectMembership(project=Project.objects.all()[0],
                          member=self.user_list[1]).save()

    def test_add_codereview(self):
        '''
        Testcase for save code review with successful patch, build and testcase
        '''
        self.assertEquals(len(CodeReview.objects.all()), 0)
        response = self.client.post(reverse('codereview:save'), {
            'code_review_id': '0',
            'project': self.project,
            'reviewer': self.user_list[0].id,
            'engineer': self.user_list[1].id,
            'review_date': '2013-02-06',
            'patch_code': '1234',
            'patch': '1',
            'build': '1',
            'testcase': '0',
            'comments': 'code review testcase for save'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(CodeReview.objects.all()), 1)

    def test_add_null_builddata(self):
        '''
        Testcase for save code review with reject patchcase.
        '''
        self.assertEquals(len(CodeReview.objects.all()), 0)
        response = self.client.post(reverse('codereview:save'), {
            'code_review_id': '0',
            'project': self.project,
            'reviewer': self.user_list[0].id,
            'engineer': self.user_list[1].id,
            'review_date': '2013-02-06',
            'patch_code': '1234',
            'patch': '1',
            'build': '',
            'testcase': '',
            'comments': 'code review testcase for save'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(CodeReview.objects.all()), 1)

    def test_add_reject_patchcase(self):
        '''
        Testcase for save code review with reject patchcase.
        '''
        self.assertEquals(len(CodeReview.objects.all()), 0)
        response = self.client.post(reverse('codereview:save'), {
            'code_review_id': '0',
            'project': self.project,
            'reviewer': self.user_list[0].id,
            'engineer': self.user_list[1].id,
            'review_date': '2013-02-06',
            'patch_code': '1234',
            'patch': '0',
            'comments': 'code review testcase for save'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(CodeReview.objects.all()), 1)

    def test_update_existing_codereview(self):
        self.test_add_codereview()
        response = self.client.post(reverse('codereview:save'), {
            'code_review_id': CodeReview.objects.all()[0].id,
            'project': self.project,
            'reviewer': self.user_list[0].id,
            'engineer': self.user_list[1].id,
            'review_date': '2013-02-06',
            'patch_code': '1234',
            'patch': '1',
            'build': '1',
            'testcase': '0',
            'comments': 'code review testcase for update'})
        self.assertEquals(response.status_code, 302)
        code_review = CodeReview.objects.all()
        self.assertEquals(len(code_review), 1)
        self.assertEquals(code_review[0].comments,
                          'code review testcase for update')

    def test_view_codereview(self):
        self.test_add_codereview()
        response = self.client.post(reverse('codereview:edit', args=[
                                    str(CodeReview.objects.all()[0].id)]))
        self.assertEquals(response.status_code, 200)

    def test_get_team_members(self):
        self.test_add_codereview()
        response = self.client.post(reverse('codereview:get_team_members',
                                            args=[str(self.project)]))
        self.assertEquals(response.status_code, 200)

    def test_get_allprojects_team_members(self):
        self.test_add_codereview()
        response = self.client.post(reverse('codereview:get_team_members'))
        self.assertEquals(response.status_code, 200)

    def test_codereview_list(self):
        self.test_add_codereview()
        response = self.client.post(reverse('codereview:list'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            len(response.context['page_data']['code_review']), 1)

    def test_search_list(self):
        self.test_add_codereview()
        response = self.client.post(
            reverse('codereview:list') + "?search=search", {
                'search_project': self.project,
                'search_reviewer': self.user_list[0].id,
                'search_engineer': self.user_list[1].id,
                'from_date': '2013-02-01',
                'to_date': '2013-02-07',
                'search_build': '1',
                'search_patch': '1',
                'search_testcase': '0', })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            len(response.context['page_data']['code_review']), 1)

    def test_search_invalid_list(self):
        self.test_add_codereview()
        response = self.client.post(
            reverse('codereview:list') + "?search=search", {
                'search_project': self.project,
                'search_reviewer': self.user_list[0].id,
                'search_engineer': self.user_list[1].id,
                'from_date': '2013-02-01',
                'to_date': '2013-02-07',
                'search_build': '0',  # change path filter option.
                'search_patch': '1',
                'search_testcase': '0', })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            len(response.context['page_data']['code_review']), 0)

    def test_search_with_project(self):
        self.test_add_codereview()
        response = self.client.post(
            reverse('codereview:list') + "?search=search", {
                'search_project': self.project})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            len(response.context['page_data']['code_review']), 1)
        self.assertEquals(
            response.context['page_data']['code_review'][0].project.id,
            self.project)

    def test_search_with_project(self):
        self.test_add_codereview()
        response = self.client.post(
            reverse('codereview:list') + "?search=search", {
                'search_project': self.project})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            len(response.context['page_data']['code_review']), 1)
        self.assertEquals(
            response.context['page_data']['code_review'][0].project.id,
            self.project)
