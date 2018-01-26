from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from project_management.projectbudget.models import *
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext, Context, loader
# from django.utils import simplejson
try:
    import django.utils.simplejson
except BaseException:
    import json as simplejson

from django.shortcuts import render


@login_required
def phase_list(request):
    query = Q()
    searchtext = request.GET.get('search', '')
    json_msg = request.GET.get('msg')
    if(json_msg is None):
        json_msg = ""
#    if ((searchtext == " ") | (searchtext == "  ")):
#        searchtext == " ";
    if searchtext:
        for term in searchtext.split():
            q = Q(phase__icontains=term) | Q(code__icontains=term)
            print q

        query = query & q
#        print query
    phase_details = BudgetPhase.objects.filter(
        query).exclude(is_active=False)
    return render(
        request, 'phase.html', {
            'phase_details': phase_details, 'json_msg': json_msg})


@login_required
def delete_phase(request):
    msg = ''
    bg_color = ''
    color = ''
    phase_id = request.POST.getlist('check')
    for i in phase_id:
        val_check = ProjectBudgetEfforts.objects.filter(phase=i)
        if len(val_check) == 0:
            delete_phase = BudgetPhase.objects.filter(pk=i).update(is_active=0)
            msg = "Phase Deleted Successfully"
            bg_color = "#5AECBF"
            color = "#000000"
        else:
            msg = "Phase used in Budget, Unable to delete this Phase"
            bg_color = "#FF0000"
            color = "#FFFFFF"
    phase_details = BudgetPhase.objects.filter(is_active=1)
    return render(request,
                  'phase.html',
                  {'phase_details': phase_details,
                   'msg': msg,
                   'bg_color': bg_color,
                   'color': color},
                  )


@login_required
def create_phase(request):
    id = request.POST.get('phaseid')
    code = request.POST.get('dialog_code')
    phase = request.POST.get('dialog_phase')
    msg = ''
    #import pdb;pdb.set_trace()
    if((code is not None) and (phase is not None)):
        # print 'test',id,code,phase
        if id:
            phase_exists = BudgetPhase.objects.filter(
                Q(code=code) | Q(phase=phase)).filter(is_active=1)
            if (len(phase_exists) <= 1):
                msg = "Phase Updated Successfully"
                BudgetPhase.objects.filter(pk=id).update(code=code)
                BudgetPhase.objects.filter(pk=id).update(phase=phase)
            else:
                msg = "Code/Phase is already exist"
        else:
            phase_exists = BudgetPhase.objects.filter(
                Q(code=code) | Q(phase=phase)).filter(is_active=1)
            # print len(val_code)
            if (len(phase_exists) == 0):
                phase = BudgetPhase(code=code, phase=phase)
                phase.save()
                msg = "Phase Created Successfully"
            else:
                msg = "Code/Phase is already exist"
        phase_details = BudgetPhase.objects.filter(is_active=1)
    json = simplejson.dumps(msg)
    #json = simplejson.loads(json)
    # print json
    return HttpResponse(json, content_type='application/javascript')


@login_required
def cost_listpage(request):
    query = Q()
    searchtext = request.GET.get('search', '')
    json_msg = request.GET.get('msg')
    if(json_msg is None):
        json_msg = ""
    # if ((searchtext == " ") | (searchtext == "  ")):
        #searchtext == " ";
    if searchtext:
        for term in searchtext.split():
            q = Q(cost_type__icontains=term) | Q(code__icontains=term)
            print q

            query = query & q
    cost_list = BudgetCost.objects.filter(query).exclude(is_active=False)
    return render(request, 'cost.html', {'cost_list': cost_list,
                                         'msg': json_msg, },)
# def cost_listpage(request):
 #   cost_list = BudgetCost.objects.filter(is_active=1).order_by('-cost_type')
  #  return render(request, 'cost.html',{'cost_list':cost_list})


@login_required
def delete_cost(request):
    deleteid = request.POST.getlist('check')
    bgcolor = ''
    msg1 = ''
    color = ''
    for remove in deleteid:

        foreignid = ProjectBudgetCost.objects.filter(cost_type=remove)
        if len(foreignid) == 0:
            localid = BudgetCost.objects.filter(pk=remove).update(is_active=0)
            msg1 = "Cost deleted successfully"
            bgcolor = "#5AECBF"
            color = "#000000"
        else:
            msg1 = "Cost used in Budget, Unable to delete this Cost"
            bgcolor = "#FF0000"
            color = "#FFFFFF"
    cost_list = BudgetCost.objects.filter(is_active=1)
    return render(
        request, 'cost.html', {
            'cost_list': cost_list, 'msg1': msg1, 'bgcolor': bgcolor, 'color': color, },)


@login_required
def add_cost(request):
    id = request.POST.get('costid')
    code = request.POST.get('code')
    cost = request.POST.get('cost_type')
    msg = ''

    if((code is not None) and (cost is not None)):

        if id:
            cost_exists = BudgetCost.objects.filter(
                Q(code=code) | Q(cost_type=cost)).filter(is_active=1)
            if (len(cost_exists) <= 1):
                msg = "Cost Updated Successfully"
                BudgetCost.objects.filter(pk=id).update(code=code)
                BudgetCost.objects.filter(pk=id).update(cost_type=cost)
            else:
                msg = "Code/Cost type is already exist"
        else:
            cost_exists = BudgetCost.objects.filter(
                Q(code=code) | Q(cost_type=cost)).filter(is_active=1)
            # print len(val_code)
            if (len(cost_exists) == 0):
                cost = BudgetCost(code=code, cost_type=cost)
                cost.save()
                msg = "Cost Created Successfully"
            else:
                msg = "Code/Cost type is already exist"
        cost_list = BudgetCost.objects.filter(is_active=1)
    json = simplejson.dumps(msg)
    #json = simplejson.loads(json)
    # print json
    return HttpResponse(json, content_type='application/javascript')

    # a={}
    #id = request.POST.get('costid')
    #code = request.POST.get('code')
    #cost = request.POST.get('cost_type')
    # if((code != None) and (cost != None)):
    #   if id:
    #      cost_exists = BudgetCost.objects.filter(is_active=1).filter(Q(code=code) | Q(cost_type=cost))
    #     if (len(cost_exists) <= 1):
    #        msg = "Cost Updated Successfully"
    #       BudgetCost.objects.filter(pk=id).update(code=code)
    #      BudgetCost.objects.filter(pk=id).update(cost_type=cost)
    #p = BudgetCost.objects.filter(pk=id).update(code=code)
    #p.update(id=id, code=code, cost_type=cost)
    # else:
    #    msg = "Code/Cost type is already exist"
#
    # else:
    #   cost_exists = BudgetCost.objects.filter(
    #      is_active=1).filter(Q(code=code) | Q(cost_type=cost))
    # if(len(cost_exists) == 0):
    #    msg = "Cost created successfully"
#
    #   c = BudgetCost(code=code, cost_type=cost)
#
#
    #  c.save()
    # print c
#
    # else:
    #   msg = "Code/Cost type is already exist"
#
    #cost_list = BudgetCost.objects.filter(is_active=1)
    #data = serializers.serialize("json", cost_list)
    #json = simplejson.dumps(msg)
    # return HttpResponse(json, mimetype='application/javascript')


@login_required
def cancel(request):
    return HttpResponseRedirect("/projectbudget/cost/")
