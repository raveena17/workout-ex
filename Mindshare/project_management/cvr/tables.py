# import django_tables2 as tables
# from .models import Cvr


# #class django_tables2.columns.LinkColumn(, urlconf=None, , kwargs=None, current_app=None, attrs=None, **extra)

# class CVRTable(tables.Table):
#     id = tables.LinkColumn(viewname='edit_cvr', args=[tables.A('pk')])
#     class Meta:
#         model = Cvr
#         exclude = ('comments', 'reason_for_visit', 'actions_taken_during_the_visit', 'next_plan_of_action',)

#         # add class="paleblue" to <table> tag
#         attrs = {'class': 'paleblue'}
