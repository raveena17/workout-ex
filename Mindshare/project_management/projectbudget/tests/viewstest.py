import re
from django.test.client import Client

from django.test import TestCase
from project_management.projectbudget.models import *
from project_management.business_unit.models import *
from project_management.projects.models import *
from project_management.projectbudget.views import budget_reminder_alertmail
from project_management import settings
from django.db.models import Max

from logintest import LoginTest


class ProjectBudgetTest(TestCase):

    urls = 'project_management.urls'
    client = Client()

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

        User.objects.create(
            id='26',
            username='admin2',
            first_name='admin2',
            last_name='',
            email='ramya@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')

        User.objects.create(
            id='28',
            username='admin1',
            first_name='admin1',
            last_name='',
            email='divya@5gindia.net',
            password='shsdsfa1$d5ec6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        self.collection_user = User.objects.all()

        response = BusinessUnit.objects.create(
            name="Project",
            firstname="XXX",
            lastname="",
            type_id="1",
            address_id="1",
            related_to_id="1",
            url="",
            contact_email="",
            notes="")
        collection = BusinessUnit.objects.all()
        id_buss_unit = collection[0].id

        ProjectSchedule.objects.create(
            expected_start_date="2012-09-20",
            expected_end_date="2012-09-25",
            planned_start_date="2012-09-20",
            planned_end_date="2012-09-25",
            approval_date="2012-09-22",
            kick_off_meeting_planned_date="2012-09-20",
            kick_off_meeting_actual_date="2012-09-20",
            actual_start_date="2012-09-20",
            actual_end_date="2012-09-20",
            initiation_request_date="2012-09-20",
            approved_date="2012-09-20",
            next_invoice_date="2012-09-20")
        collection_schedule = ProjectSchedule.objects.all()
        id_schedule = collection_schedule[0].id

        Project.objects.create(
            code="San",
            name="Test",
            short_name="S",
            business_unit_id=id_buss_unit,
            delivery_centre_id=id_buss_unit,
            parent_id="1",
            apex_body_owner_id="3",
            owner_id="2",
            approval_type="external",
            planned_effort="123",
            schedules_id=collection_schedule[0].id,
            domain_id="3",
            customer_id=id_buss_unit,
            customer_contact_id="",
            requested_by_id=self.collection_user[0].id,
            approved_by_id="1",
            other_project_type="asd",
            is_project_group="1",
            is_active="1",
            is_approved="1",
            cancel="0",
            project_type_id="2",
            project_owner_id="1",
            estimated_time_exceed="1",
            ex_approval=1,
            project_no=1)
        collection = Project.objects.all()
        self.projectid = collection[0].id

        ProjectBudget.objects.create(
            project_id=collection[0].id,
            planned_start_date="2012-09-21",
            org_end_date="2012-09-21",
            revised_start_date="2012-09-21",
            revised_end_date="2012-09-22",
            remarks="asdf",
            rejection_reason="",
            pjt_owner_id=self.collection_user[2].id,
            business_head_id=self.collection_user[1].id,
            status_id="RS1",
            version="1",
            execution_mode="asdf",
            total_effort=12.2,
            total_cost=12.500,
            other1_description="asdf",
            other2_description="qwer")
        collection = ProjectBudget.objects.all()
        self.projectversion = collection[0].version

    def test_list(self):
        response = self.client.post('/projectbudget/list/')
        self.assertEquals(response.status_code, 200)

    def test_budget_save(self):
        bud_id = ProjectBudget.objects.all()[0].id
#        print "Save"
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '5',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '',
            'revised_start_date': '28-09-2012',
            'version': 'int(1)',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS1',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'remarks': 'testcases success',
            'location1': '1',
            'phase1': '00243432-00b4-11e2-847e-00167692f6f2',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '454',
            'lead_effort1': '45443',
            'bud_id': bud_id,
            'dev_effort1': '454',
            'duration_days1': '77',
            'test_effort1': '4',
            'activity_type': '1'})
        collection = ProjectBudget.objects.all()
        version = collection[0].version
        remarks = collection[0].remarks
        self.assertEqual(version, 1)
        self.assertEqual(remarks, 'testcases success')

    def test_budget_cost_save(self):
        bud_id = ProjectBudget.objects.all()[0].id
#        print "Cost Save"
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'effort_id1': 'cbe6fd88-06dc-11e2-a045-00167692f6f2',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '0',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '2',
            'tmp_save': 'Save',
            'cost1': '500.0',
            'revised_start_date': '28-09-2012',
            'version': '1',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS1',
            'cost_id1': 'e6e58c38-06ed-11e2-b9ed-00167692fe0a',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'tot_duration': '-62',
            'cost_type1': 'c33896e6-0606-11e2-a25b-00167692f6f2',
            'remarks': '',
            'location1': '1',
            'phase1': '00243432-00b4-11e2-847e-00167692f6f2',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '0',
            'lead_effort1': '0',
            'bud_id': bud_id,
            'dev_effort1': '0',
            'duration_days1': '0',
            'test_effort1': '0',
            'activity_type': '1'})
        collection = ProjectBudget.objects.all()
        version = collection[0].version
        remarks = collection[0].remarks
        collection = ProjectBudgetCost.objects.filter(project_budget=bud_id)
#        print len(collection)
        cost = collection[0].cost
        self.assertEqual(version, 1)
        self.assertEqual(cost, 500.0)

    def test_effort_delete(self):
        bud_id = ProjectBudget.objects.all()[0].id
        response = self.client.post('/projectbudget/save/', {
            'activity_len': '3',
            'activity_type': '1',
            'bud_id': bud_id,
            'bus_head': self.collection_user[1].id,
            'cost1': '1000',
            'cost_id1': '',
            'cost_len': '2',
            'cost_type1': 'Cost1',
            'delete_cost': '',
            'delete_effort': '',
            'dev_duration': '0',
            'dev_effort1': '15',
            'dev_effort2': '15',
            'duration_days1': '10',
            'duration_days2': '10',
            'effort_id1': '',
            'effort_id2': '',
            'execution_mode': 'FixedPrice',
            'lead_effort1': '10',
            'lead_effort2': '10',
            'location1': 'Location1',
            'location2': 'Location1',
            'org_end_date': '30-09-2012',
            'oth1_effort1': '25',
            'oth1_effort2': '25',
            'oth2_effort1': '30',
            'oth2_effort2': '30',
            'other1_desc': 'Other1',
            'other2_desc': 'Other2',
            'phase1': 'Phase1',
            'phase2': 'Phase2',
            'pjt_owner': self.collection_user[2].id,
            'planned_start_date': '27-09-2012',
            'pm_effort1': '5',
            'pm_effort2': '5',
            'remarks': '',
            'revised_end_date': '30-09-2012',
            'revised_start_date': '27-09-2012',
            'status': 'RS1',
            'test_effort1': '20',
            'test_effort2': '20',
            'tmp_save': 'Save',
            'tot_duration': '-3',
            'tot_effort': '0',
            'tot_effort': '0',
            'tot_effort': '0',
            'tot_effort': '0',
            'version': '1'})
        phase = ProjectBudgetEfforts.objects.filter(project_budget=bud_id)
        print len(phase)
        phaseid = phase[0].id
        phaseid1 = phase[1].id
        cost = ProjectBudgetCost.objects.filter(project_budget=bud_id)
        costid = cost[0].id
#        print phaseid,phaseid1,costid
        response = self.client.post('/projectbudget/save/', {
            'activity_len': '3',
            'activity_type': '1',
            'bud_id': bud_id,
            'bus_head': self.collection_user[1].id,
            'cost1': '1000',
            'cost_id1': costid,
            'cost_len': '2',
            'cost_type1': 'Cost1',
            'delete_cost': '',
            'delete_effort': phaseid,
            'dev_duration': '0',
            'dev_effort1': '15',
            'dev_effort2': '15',
            'duration_days1': '10',
            'duration_days2': '10',
            'effort_id1': phaseid,
            'effort_id2': phaseid1,
            'execution_mode': 'FixedPrice',
            'lead_effort1': '10',
            'lead_effort2': '10',
            'location1_id': 'Location1',
            'location2_id': 'Location1',
            'org_end_date': '30-09-2012',
            'oth1_effort1': '25',
            'oth1_effort2': '25',
            'oth2_effort1': '30',
            'oth2_effort2': '30',
            'other1_desc': 'Other1',
            'other2_desc': 'Other2',
            'phase1': 'Phase1',
            'phase2': 'Phase2',
            'pjt_owner': self.collection_user[2].id,
            'planned_start_date': '27-09-2012',
            'pm_effort1': '5',
            'pm_effort2': '5',
            'remarks': '',
            'revised_end_date': '30-09-2012',
            'revised_start_date': '27-09-2012',
            'status': 'RS1',
            'test_effort1': '20',
            'test_effort2': '20',
            'tmp_save': 'Save',
            'tot_duration': '-3',
            'tot_effort': '0',
            'tot_effort': '0',
            'tot_effort': '0',
            'tot_effort': '0',
            'version': '1'})
        phase = ProjectBudgetEfforts.objects.filter(project_budget=bud_id)
        len_phase = len(phase)
        print len_phase
        self.assertEqual(len_phase, 1)

    def test_cost_delete(self):
        bud_id = ProjectBudget.objects.all()[0].id
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'effort_id1': '',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '0',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '2',
            'tmp_save': 'Save',
            'cost1': '500.0',
            'revised_start_date': '28-09-2012',
            'version': '1',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS1',
            'cost_id1': '',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'tot_duration': '-62',
            'cost_type1': 'Cost',
            'remarks': '',
            'location1': '1',
            'phase1': 'Phase1',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '0',
            'lead_effort1': '0',
            'bud_id': bud_id,
            'dev_effort1': '0',
            'duration_days1': '0',
            'test_effort1': '0',
            'activity_type': '1'})
        # print bud_id
        cost = ProjectBudgetCost.objects.filter(project_budget=bud_id)
        costid = cost[0].id
        # print costid
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'effort_id1': 'cbe6fd88-06dc-11e2-a045-00167692f6f2',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '0',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': costid,
            'cost_len': '1',
            'tmp_save': 'Save',
            'revised_start_date': '28-09-2012',
            'version': '1',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS1',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'tot_duration': '-62',
            'cost_type1': 'c33896e6-0606-11e2-a25b-00167692f6f2',
            'remarks': '',
            'location1': '1',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '0',
            'lead_effort1': '0',
            'bud_id': bud_id,
            'dev_effort1': '0',
            'duration_days1': '0',
            'test_effort1': '0',
            'activity_type': '1'})
        cost = ProjectBudgetCost.objects.filter(project_budget=bud_id)
        len_cost = len(cost)
        print len_cost
        self.assertEqual(len_cost, 0)

    def test_budget_creation(self):
        self.test_budget_approve()
        bud_id = ProjectBudget.objects.all()[0].id
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '225',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '',
            'revised_start_date': '28-09-2012',
            'version': 'int(1)',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS1',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'remarks': 'testcases success',
            'location1': '1',
            'phase1': '00243432-00b4-11e2-847e-00167692f6f2',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '454',
            'lead_effort1': '45443',
            'bud_id': bud_id,
            'dev_effort1': '454',
            'duration_days1': '3477',
            'test_effort1': '344',
            'activity_type': '1'})
        response = self.client.get('/projectbudget/create/', {
            'pjt_id': self.projectid,
            'version': '2'})
        bud_version = ProjectBudget.objects.filter(
            project__id=self. projectid).aggregate(
            Max('version')).get('version__max')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(str(bud_version), '2')

    def test_budget_approve(self):
        bud_id = ProjectBudget.objects.all()[0].id
#        print "Approve"
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'effort_id1': 'cbe6fd88-06dc-11e2-a045-00167692f6f2',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '0',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '2',
            'tmp_save': 'Save',
            'cost1': '500.0',
            'cost_approved': '1',
            'revised_start_date': '28-09-2012',
            'version': '1',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS4',
            'cost_id1': 'e6e58c38-06ed-11e2-b9ed-00167692fe0a',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'tot_duration': '-62',
            'cost_type1': 'c33896e6-0606-11e2-a25b-00167692f6f2',
            'remarks': '',
            'location1': '1',
            'phase1': '00243432-00b4-11e2-847e-00167692f6f2',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '0',
            'lead_effort1': '0',
            'bud_id': bud_id,
            'dev_effort1': '0',
            'duration_days1': '0',
            'effort_approved': '1',
            'test_effort1': '0',
            'activity_type': '1'})
        collection = ProjectBudget.objects.all()
        status = collection[0].status.id
#        print status
        self.assertEqual(str(status), 'RS4')

    def test_budget_reject(self):
        bud_id = ProjectBudget.objects.all()[0].id
#        print "Reject"
        response = self.client.post('/projectbudget/save/', {
            'execution_mode': 'FixedPrice',
            'effort_id1': 'cbe6fd88-06dc-11e2-a045-00167692f6f2',
            'bus_head': self.collection_user[1].id,
            'oth1_effort1': '0',
            'activity_len': '2',
            'dev_duration': '0',
            'delete_effort': '',
            'delete_cost': '',
            'cost_len': '2',
            'tmp_save': 'Save',
            'cost1': '500.0',
            'cost_approved': '1',
            'revised_start_date': '28-09-2012',
            'version': '1',
            'revised_end_date': '29-11-2012',
            'org_end_date': '29-11-2012',
            'other1_desc': 'Other1',
            'status': 'RS5',
            'cost_id1': 'e6e58c38-06ed-11e2-b9ed-00167692fe0a',
            'pm_effort1': '0',
            'planned_start_date': '28-09-2012',
            'other2_desc': 'Other2',
            'tot_duration': '-62',
            'cost_type1': 'c33896e6-0606-11e2-a25b-00167692f6f2',
            'remarks': '',
            'location1': '1',
            'phase1': '00243432-00b4-11e2-847e-00167692f6f2',
            'pjt_owner': self.collection_user[2].id,
            'oth2_effort1': '0',
            'lead_effort1': '0',
            'bud_id': bud_id,
            'dev_effort1': '0',
            'duration_days1': '0',
            'effort_approved': '1',
            'test_effort1': '0',
            'activity_type': '1',
            'rjt_reason': 'Rejected'})
        collection = ProjectBudget.objects.all()
        status = collection[0].status.id
#        print status
        Reason = collection[0].rejection_reason
#        print Reason
        self.assertEqual(str(status), 'RS5')
        self.assertEqual(Reason, 'Rejected')

    def test_reminder_mail(self):
        budget_reminder_alertmail(self)

    def test_budget_export(self):
        pjt_id = self.projectid
        version = self.projectversion
        print pjt_id, version
        response = self.client.get('/projectbudget/export_budget/',
                                   {'pjt_id': pjt_id, 'version': '1'})
        print response.status_code
