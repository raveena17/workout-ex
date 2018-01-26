# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render
# from django_tables2 import RequestConfig
# # from django.core.context_processors import csrf
# from django.template.context_processors import csrf
# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect
# from django.core.urlresolvers import reverse
# from django.utils import timezone
# from django.views.generic import UpdateView
# from django.contrib.auth.decorators import login_required
# # from django.contrib.auth.mixins import LoginRequiredMixin
# from cvr.form import cvrTableForm
# from cvr.tables import CVRTable
# from cvr.models import Cvr


# def table(request):
#     # import pdb;pdb.set_trace()
#     cvr_table = CVRTable(Cvr.objects.all())
#     RequestConfig(request).configure(cvr_table)
#     return render(request, 'cvr/table.html', {'table': cvr_table})


# # @login_required
# def post_new(request):
#     # import pdb;pdb.set_trace()
#     print(request.user.username)

#     if request.POST:
#         form = cvrTableForm(request.POST)
#         if form.is_valid():
#             cvr_item = form.save(commit=False)
#             cvr_item.prepared_by = request.user.username #change it for request user
#             cvr_item.save()
#             return redirect(reverse('table'))
#         # return redirect(reverse("post_new/"))

#     else:
#         form = cvrTableForm()

#     context = {
#         'form': form,
#         'action': 'Submit'
#     }

#     return render(request, "cvr/cvr_form.html", context)


# class CvrUpdateView(UpdateView):
#     model = Cvr
#     form_class = cvrTableForm

#     def get_success_url(self):
#         # This will be a different view
#         return reverse('table')

#     def get_context_data(self, **kwargs):
#         context_data = super(CvrUpdateView, self).get_context_data(**kwargs)
#         context_data['action'] = 'Approve'
#         return context_data

#     def post(self, request, *args, **kwargs):
#         result = super(CvrUpdateView, self).post(request, *args, **kwargs)
#         print(self.object)
#         if self.object:
#             self.object.approved_by = request.user.username
#             self.object.date_of_approval = timezone.now()
#             self.object.save()
#         return result
