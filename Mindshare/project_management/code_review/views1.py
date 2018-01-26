# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
# from django.utils import simplejson
try:
    import django.utils.simplejson
except:
    import json as simplejson

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db.models import Q
from datetime import datetime

from project_management.code_review.models import *
from project_management.projects.models import ProjectMembership


@login_required
def edit(request, code_review_id):
    code_review = CodeReview.objects.filter(id=code_review_id)
    team_members = Project.objects.get(\
        id=code_review[0].project.id).team.filter(is_active=1).order_by('first_name')
    code_review_json = serializers.serialize("json", code_review)
    team_members_json = serializers.serialize("json", team_members)
    code_review_dict = [{
        'code_review':code_review_json,
        'team_members':team_members_json}]
    json = simplejson.dumps(code_review_dict)
    return HttpResponse(json, mimetype='application/json')


@login_required
def get_team_members(request, project_id=None):
    if project_id != '' and project_id != None:
        '''
        Get team members for selected project
        '''
        team_members = Project.objects.get(\
            id=project_id).team.filter(is_active=1).distinct().order_by('first_name')
    else:
        '''
        Get team members of a login user's all project, which are he included
        '''
        team_member_list = []
        [team_member_list.extend(each.team.filter(is_active=1).distinct().order_by(\
            'first_name')) for each in
            Project.objects.filter(Q(apex_body_owner=request.user) |
            Q(owner=request.user) |
            Q(team=request.user) | Q(requested_by = request.user))\
            .filter(is_active=1).distinct().exclude(cancel=True)]
        team_members = set(team_member_list)
    data = serializers.serialize("json", team_members)
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/javascript')


@login_required
def save_review(request):
    patch = int(request.POST.get('patch'))\
        if request.POST.get('patch') else None
    code_review = CodeReview.objects.filter(\
        id=request.POST.get('code_review_id', ''))
    code_review_dict = {
        'id': None if len(code_review) == 0 else code_review[0].id,
        'reviewer_id': request.POST.get('reviewer', ''),
        'engineer_id': request.POST.get('engineer', ''),
        'project_id': request.POST.get('project', ''),
        'review_date': request.POST.get('review_date', ''),
        'patch_code': request.POST.get('patch_code', ''),
        'patch': patch,
        'build': int(request.POST.get('build'))
            if patch == 1 and request.POST.get('build') else None,
        'test_case': int(request.POST.get('testcase'))
            if patch == 1 and request.POST.get('testcase') else None,
        'comments': request.POST.get('comments', ''),
        'modified_by_id': request.user.id,
        'created_by_id': request.user.id
            if len(code_review) == 0 else code_review[0].created_by.id,
        'created_on': datetime.now().date()
            if len(code_review) == 0 else code_review[0].created_on,
        }
    code_review = CodeReview(**code_review_dict)
    code_review.save()
    return HttpResponseRedirect(reverse('codereview:list'))


@login_required
def code_review_list(request):
    selected_project = ''
    selected_eng = ''
    search_reviewer = ''
    selected_patch = ''
    selected_build = ''
    selected_testcase = ''
    selected_from_date = ''
    selected_to_date = ''

    '''
    Get last updated code review's project, team and engineer.
    '''
    last_updated_pjt = ''
    code_review_list = CodeReview.objects.filter(\
        reviewer=request.user.id).order_by('-modified_on')
    last_updated_pjt_team = []
    last_updated_eng = ''
    if len(code_review_list) > 0:
        last_updated_pjt = code_review_list[0].project.id
        last_updated_eng = code_review_list[0].engineer.id
        last_updated_pjt_team = Project.objects.get(is_active=1,
            id=last_updated_pjt).team.filter(is_active=1).distinct().order_by(\
            'first_name')
    query = Q(is_active = True) & Q(project__in = Project.objects.filter(\
                Q(apex_body_owner=request.user) |
                Q(owner=request.user) |
                Q(team=request.user) | Q(requested_by = request.user))\
                .filter(is_active=True).distinct().exclude(cancel=True).values('id'))
    if request.GET.get('search') == 'search':
        '''
        Form filter query for code review list, with search options.
        '''
        selected_from_date = request.POST.get('from_date', '')
        selected_to_date = request.POST.get('to_date', '')
        if request.POST.get('search_project', '') != '':
            selected_project = Project.objects.get(is_active=1,\
                id=request.POST.get('search_project', '')).id
            query = query & Q(project = selected_project)
        if request.POST.get('search_engineer', '') != '':
            selected_eng = User.objects.get(is_active=1,\
                id=request.POST.get('search_engineer', '')).id
            query = query & Q(engineer = selected_eng)
        if request.POST.get("search_reviewer", '') != '':
            search_reviewer = User.objects.get(is_active=1,\
                id=request.POST.get("search_reviewer", '')).id
            query = query & Q(reviewer = search_reviewer)
        if selected_from_date != '':
            query = query & Q(review_date__gte = selected_from_date)
        if selected_to_date != '':
            query = query & Q(review_date__lte = selected_to_date)
        if request.POST.get("search_patch", '') != '':
            selected_patch = request.POST.get("search_patch", '')
            query = query & Q(patch = selected_patch
            if selected_patch != '2' else None)
        if request.POST.get("search_build", '') != '':
            selected_build = request.POST.get("search_build", '')
            query = query & Q(build = selected_build
            if selected_build != '2' else None)
        if request.POST.get("search_testcase", '') != '':
            selected_testcase = request.POST.get("search_testcase", '')
            query = query & Q(test_case = selected_testcase
            if selected_testcase != '2' else None)

    else:
        '''
        Form filter query with last entered project for code
        review and login user
        '''
        search_reviewer = request.user.id
        query = query & Q(reviewer = search_reviewer)
        if len(code_review_list) > 0:
            selected_project = last_updated_pjt
            query = query & Q(project = selected_project)
    code_review = CodeReview.objects.filter(\
        query).order_by('-modified_on')
    projects = Project.objects.filter(Q(apex_body_owner=request.user) |
            Q(owner=request.user) |
            Q(team=request.user) | Q(requested_by = request.user))\
            .filter(is_active=1).distinct().exclude(cancel=True)
    if selected_project != '':
        '''
        Get team_members of login user's last entered project .
        '''
        team_members = Project.objects.get(is_active=1, id=selected_project).\
            team.filter(is_active=1).distinct().order_by('first_name')
    else:
        '''
        At the first time access of code review page, get team members of a
        login user's all project, which are he included
        '''
        team_member_list = []
        [team_member_list.extend(each.team.filter(is_active=1).distinct().order_by(\
            'first_name')) for each in
            Project.objects.filter(Q(apex_body_owner=request.user) |
            Q(owner=request.user) |
            Q(team=request.user) | Q(requested_by = request.user))\
            .filter(is_active=1).distinct().exclude(cancel=True)]
        team_members = set(team_member_list)
    page_data = {
        'projects': projects,
        'code_review': code_review,
        'team_members': team_members,
        'selected_project': selected_project,
        'search_reviewer': search_reviewer,
        'selected_eng': selected_eng,
        'selected_patch': selected_patch,
        'selected_build': selected_build,
        'selected_testcase': selected_testcase,
        'selected_from_date': selected_from_date,
        'selected_to_date': selected_to_date,
        'last_updated_pjt': last_updated_pjt,
        'last_updated_pjt_team': last_updated_pjt_team 
            if len(last_updated_pjt_team) > 0 else team_members,
        'last_updated_eng': last_updated_eng,
        }
    return render(request, 'code_review.html', {'page_data': page_data},
        )
