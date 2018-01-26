"""
    views for users application
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
# from django.shortcuts import render_to_response
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
#from django.views.generic import list_detail
from django.contrib.auth.decorators import permission_required
from django.core.files.uploadedfile import SimpleUploadedFile

from project_management.users.models import UserProfile
from project_management.users.forms import UserProfileForm, UserForm, \
    MyProfileForm
from project_management.address.forms import AddressForm
from django.views.generic import RedirectView


@csrf_protect
@never_cache
def login(request, template_name='login.html',
          authentication_form=AuthenticationForm):
    "Displays the login form and handles the login action."
    RedirectView = settings.USER_REDIRECT_URL
    if request.method == "POST":
        request.session['localTimeZone'] = request.POST.get(
            'localTimeZone', '')
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # imported inside login to prevent override
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.user and request.user.is_staff:
                RedirectView = settings.ADMIN_REDIRECT_URL
            return HttpResponseRedirect(RedirectView)
    else:
        form = authentication_form(request)
    return render(request, template_name, {
        'form': form},)


@login_required
@permission_required('users.add_userprofile')
def user_list(request, page=1, msg=''):
    """
        Display the list of users.
    """

    query = Q(user__is_active=True)

    searchtext = request.GET.get('search', '')
    show_inactive = request.GET.get('is_active', '0')

    if searchtext:
        for term in searchtext.split():
            q = Q(user__first_name__icontains=term)
        query = query & q

    if int(show_inactive):
        query = query | Q(user__is_active=False)

    return list_detail.object_list(
        request,
        queryset=UserProfile.objects.filter(
            query, user__is_staff=False).exclude(
            type='CC').order_by('-code'),
        template_name="user_list.html",
        template_object_name="user",
        extra_context={'show_inactive': int(show_inactive)}
    )


@login_required
@permission_required('users.add_userprofile')
def manage_user(request, pid=None, RedirectView=user_list):
    """
        Add/Edit user.
    """

    profile = user = address_contact = address_permanent = users_image = business_unit = None
    check_list = business_unit_list = firstname = lastname = emailid = userName = Contact_address = Permanent_address = role = reporting_senior = None
    file_data = {}
    if pid:

        profile = get_object_or_404(UserProfile, pk=pid)
        user = profile.user
        address_contact = profile.address_contact
        address_permanent = profile.address_permanent
        users_image = profile.users_image
        check_list = profile.document_check_list.all()
        business_unit_list = profile.business_unit.all()
        firstname = profile.user.first_name
        lastname = profile.user.last_name
        emailid = profile.user.email
        userName = profile.user.username
        Contact_address = profile.address_contact
        Permanent_address = profile.address_permanent
        reporting_senior_name = profile.reporting_senior_name
        role = profile.user.groups.all()

        if profile.confirmation_status == 'CONFIRMED':
            profile.is_confirmed = True
        else:
            profile.is_confirmed = False

    if request.method == 'POST':
        if request.FILES:
            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=profile)
        else:
            file_data = None
            profile_form = UserProfileForm(
                request.POST, file_data, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        address_contact_form = AddressForm(request.POST,
                                           instance=address_contact, prefix='contact')
        address_permanent_form = AddressForm(request.POST,
                                             instance=address_permanent, prefix='permanent')

        if profile_form.is_valid() and address_contact_form.is_valid() \
                and user_form.is_valid() and address_permanent_form.is_valid():
            address_contact = address_contact_form.save()
            address_permanent = address_permanent_form.save()
            user = user_form.save()
            profile_form.save(user=user, address_contact=address_contact,
                              address_permanent=address_permanent)

            messages.success(request, _('User saved successfully.'))
            return HttpResponseRedirect(reverse(RedirectView))
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserForm(instance=user)
        address_contact_form = AddressForm(instance=address_contact,
                                           prefix='contact')
        address_permanent_form = AddressForm(instance=address_permanent,
                                             prefix='permanent')

    return render(request, 'user.html', {'profile': profile,
                                         'user_form': user_form, 'profile_form': profile_form,
                                         'address_contact_form': address_contact_form,
                                         'address_permanent_form': address_permanent_form,
                                         'users_image': users_image, 'check_list': check_list, 'business_unit_list': business_unit_list,
                                         'firstname': firstname, 'lastname': lastname, 'emailid': emailid, 'userName': userName,
                                         'Contact_address': Contact_address, 'Permanent_address': Permanent_address, 'role': role,
                                         'reporting_senior': reporting_senior},
                  )


@login_required
def manage_myprofile(request):
    """
        Modification of profile of the user.
    """
    profile = request.user.get_profile()
    users_image = profile.users_image
    if not profile:
        raise Http404
    if request.method == 'POST':
        profile_form = MyProfileForm(request.POST, instance=profile)
        address_contact_form = AddressForm(request.POST,
                                           instance=profile.address_contact, prefix='contact')
        address_permanent_form = AddressForm(request.POST,
                                             instance=profile.address_permanent, prefix='permanent')

        if profile_form.is_valid() and address_contact_form.is_valid() \
                and address_permanent_form.is_valid():
            address_contact = address_contact_form.save()
            address_permanent = address_permanent_form.save()

            profile_form.save(address_contact=address_contact,
                              address_permanent=address_permanent)
            messages.success(request,
                             _('your profile details saved sucessfully'))
    else:
        profile_form = MyProfileForm(instance=profile)
        address_contact_form = AddressForm(instance=profile.address_contact,
                                           prefix='contact')
        address_permanent_form = AddressForm(
            instance=profile.address_permanent, prefix='permanent')

    return render(request, 'myprofile.html', {
        'profile_form': profile_form,
        'address_contact_form': address_contact_form,
        'address_permanent_form': address_permanent_form,
        'users_image': users_image
    },
    )


@login_required
@permission_required('users.add_userprofile')
def manage_user_status(request, status=None):
    """
        Activate/Deactivate the users.
    """
    if request.method == 'POST':
        profiles = request.POST.getlist('user_pk')
        try:
            for profile_id in profiles:
                user = UserProfile.objects.get(pk=profile_id).user
                user.is_active = status
                user.save()
            messages.success(
                request, _('User(s) status changed successfully.'))
        except Exception:
            messages.error(request, _('Users(s) status change Failed'))
    return HttpResponseRedirect(reverse(user_list))
