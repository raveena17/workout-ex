import re
from django.test.client import Client

from django.test import TestCase
from project_management.projectbudget.models import *
from project_management.business_unit.models import *
from project_management import settings

from logintest import LoginTest


class CostTest(TestCase):
    client = Client()

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

    def test_costlink(self):
        response = self.client.get('/projectbudget/cost/')
        self.assertEqual(response.status_code, 200)

    def test_save_cost(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        self.assertEqual(response.status_code, 200)

    def test_cost_check(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': 'Cost1',
                                    'cost_type': 'Local Travel costs'})
        collection = BudgetCost.objects.all()
        code = collection[0].code
        cost_type = collection[0].cost_type
        self.assertEqual(code, 'Cost1')
        self.assertEqual(cost_type, 'Local Travel costs')
        self.assertEqual(response.status_code, 200)

    def test_delete_cost(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/cost/delete/', {
                                    'check': id,
                                    'costid': '',
                                    'code': '',
                                    'cost_type': ''})
        self.assertEqual(response.status_code, 200)

    def test_edit_cost(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': id,
                                    'code': '456',
                                    'cost_type': 'efgh'})
        collection = BudgetCost.objects.all()
        self.assertEqual(response.status_code, 200)

    def test_edit_cost_check(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': id,
                                    'code': '456',
                                    'cost_type': 'efgh'})
        collection = BudgetCost.objects.all()
        code = collection[0].code
        cost_type = collection[0].cost_type
        self.assertEqual(code, '456')
        self.assertEqual(cost_type, 'efgh')

    def test_cost_duplication_check(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        message = response.content
        self.assertEqual(message, '"Code/Cost type is already exist"')

    def test_dependency_check(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'Test'})
        collection = BudgetCost.objects.all()
        id = collection[0].id
        response = ProjectBudgetCost.objects.create(
            project_budget_id="123",
            cost_type_id=id,
            cost="123")
        response = self.client.post('/projectbudget/cost/delete/', {
                                    'check': id,
                                    'costid': '',
                                    'code': '',
                                    'cost_type': ''})
        message = response.context['msg1']
        self.assertEqual(message,
                         "Cost used in Budget, Unable to delete this Cost")


class InvalidCostTest(TestCase):

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

    def test_invalid_add_cost(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        code = collection[0].code
        cost_type = collection[0].cost_type
        self.assertNotEqual(code, '456')
        self.assertNotEqual(cost_type, 'efgh')

    def test_invalid_edit_cost(self):
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': '',
                                    'code': '123',
                                    'cost_type': 'abcd'})
        collection = BudgetCost.objects.all()
        id = collection[0].id
        response = self.client.post('/projectbudget/cost/add/', {
                                    'costid': id,
                                    'code': '456',
                                    'cost_type': 'efgh'})
        collection = BudgetCost.objects.all()
        code = collection[0].code
        cost_type = collection[0].cost_type
        self.assertNotEqual(code, '123')
        self.assertNotEqual(cost_type, 'abcd')
