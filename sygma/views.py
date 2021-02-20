# import decimal
# from datetime import datetime, timedelta
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, GrantmakerForm, GrantForm,\
                   StatusForm, ObligationForm
from .util import is_valid_id, get_or_post_only, get_method_only,\
                  post_method_only, invalid_id, does_not_exist
from .models import Grantmaker, Grant, Status, Obligation


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'sygma/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'sygma/dashboard.html',
                  {'section': 'dashboard'})


def grantmaker_view(request):
    template_path = 'sygma/grantmaker.html'

    def blank_form(req):
        """Render the template with a blank form"""
        context = {
            "form": GrantmakerForm(auto_id=True)
        }
        return render(req, template_path, context)

    def populated_form(req, f):
        """Render the template with a populated form"""
        context = {
            "form": f
        }
        return render(req, template_path, context)

    def create_or_update(req):
        """Updates a grantmaker from the form if it exists, or otherwise creates it."""
        f = GrantmakerForm(data=req.POST)

        if f.is_valid():
            gm_id = req.POST.get('id', None)
            if gm_id == '' or gm_id is None:
                new_gm = f.save()
                return redirect('/sygma/grantmaker?id=' + str(new_gm.id))

            elif is_valid_id(gm_id):
                # Update the specified grantmaker
                gm_id = int(gm_id)
                try:
                    # Select that grantmaker
                    gm = Grantmaker.objects.get(pk=gm_id)

                    # Apply all changes submitted with the form and save
                    for k, v in f.cleaned_data.items():
                        setattr(gm, k, v)
                    gm.save()

                    # Return to this grantmaker's detail view
                    return redirect('/sygma/grantmaker?id=' + str(gm.pk))

                except Grantmaker.DoesNotExist:
                    # Return a 404 if that grantmaker doesn't exist
                    return HttpResponse("Grantmaker {} not found".format(str(gm_id)),
                                        status=404)
            else:
                # Return a 400 if the specified id is invalid
                return invalid_id()
        else:
            # Return a 400 if form validation fails
            return HttpResponse("Form data is invalid",
                                status=400)

    if request.method == 'GET':
        gm_id = request.GET.get('id', None)
        if gm_id == '' or gm_id is None:
            # Return a blank grantmaker form if no id is specified
            return blank_form(request)

        elif is_valid_id(gm_id):
            # Return a populated page for the specified grantmaker
            gm_id = int(gm_id)
            try:
                gm = Grantmaker.objects.get(pk=gm_id)
                form = GrantmakerForm(instance=gm)
                return populated_form(request, form)
            except Grantmaker.DoesNotExist:
                return does_not_exist(gm_id, 'Grant')
        else:
            # Return a 400 if the specified id is invalid
            # raise ValueError(gm_id)
            return invalid_id()

    elif request.method == 'POST':
        return create_or_update(request)

    else:
        # Return a 405 for unsupported methods
        return get_or_post_only()


def grantmaker_list(request):
    # TODO: Could we do some ModelForm trickery to render it nicely?
    # TODO: In each table row, include a view/edit link (eventually button)
    template_path = 'sygma/grantmakers.html'

    def render_response():
        rows = Grantmaker.objects.all()
        list_vals = [{"id": r.pk,
                      "name": r.name,
                      "kind": r.kind,
                      "city": r.city,
                      "state": r.state}
                     for r in rows]
        context = {
            'grantmakers': list_vals
        }
        return render(request, template_path, context)

    if request.method == 'GET':
        return render_response()
    else:
        return get_method_only()


def grant_view(request):
    template_path = 'sygma/grant.html'

    def blank_form(req):
        # Render the template with a blank form
        context = {
            "form": GrantForm(auto_id=True)
        }
        return render(req, template_path, context)

    def populated_form(req, f):
        # Render the template with a populated form
        context = {
            "form": f
        }
        return render(req, template_path, context)

    def create_or_update(req):
        """INSERT or UPDATE a grant with an optional id, so long as form data is valid."""
        f = GrantForm(data=req.POST)
        # TODO: This will break on Grantmaker.DoesNotExist
        gm = Grantmaker.objects.get(pk=req.POST.get('grantmaker', None))

        if f.is_valid():
            # Create or update the specified grant
            grant_id = req.POST.get('id', None)
            if grant_id == '':
                # Create a grant, including its specified grantmaker
                f.save(commit=False)
                f.grantmaker = gm
                new_grant = f.save()
                return redirect('/sygma/grant?id=' + str(new_grant.pk))

            elif is_valid_id(grant_id):
                # Update the specified grant
                grant_id = int(grant_id)
                try:
                    # If it exists, save the changes and return to grant view
                    g = Grant.objects.get(pk=grant_id)
                    for k, v in f.cleaned_data.items():
                        setattr(g, k, v)
                    g.save()

                    return redirect('/sygma/grant?id=' + str(grant_id))
                except Grant.DoesNotExist:
                    # Otherwise, return a 404
                    return does_not_exist(grant_id, 'Grant')

            else:
                # Return a 400 if id is given but invalid
                return invalid_id()
        else:

            # Return a 400 if the form data fails to validate
            return HttpResponse("Form data is invalid",
                                status=400)

    if request.method == 'GET':
        grant_id = request.GET.get('id', None)

        if grant_id == '' or grant_id is None:
            return blank_form(request)

        elif is_valid_id(grant_id):
            try:
                grant = Grant.objects.get(pk=grant_id)
                form = GrantForm(instance=grant)
                return populated_form(request, form)

            except Grant.DoesNotExist:
                return does_not_exist(grant_id, 'Grant')

        else:
            return invalid_id()
    elif request.method == 'POST':
        # Save it if it's valid and return a populated form,
        # or return a 400 if it's not.
        return create_or_update(request)
    else:
        return get_or_post_only()


def grant_list(request):
    template_path = 'sygma/grants.html'

    def render_response():
        rows = Grant.objects.all()
        list_vals = [{"id": r.pk,
                      "grantmaker": r.grantmaker.name,
                      "name": r.name,
                      "restricted": r.restricted}
                     for r in rows]
        context = {
            'grants': list_vals
        }
        return render(request, template_path, context)

    if request.method == 'GET':
        return render_response()
    else:
        return get_method_only()


def status(request):
    # TODO: Statuses should be automatically assigned
    #       the grant id of their parent grant.
    template_path = 'sygma/status.html'

    def blank_form(req):
        # Render the template with a blank form
        context = {
            "form": StatusForm(auto_id=True)
        }
        return render(req, template_path, context)

    def populated_form(req, f):
        context = {"form": f}
        return render(req, template_path, context)

    def refresh_grant_page(req, grant_id):
        # Refresh the Grant page with the updated Status
        # TODO: Preserve the user's filter and sort settings
        #       for the table of statuses (and obligations?)
        return redirect("/sygma/grant?id=" + str(grant_id))

    def create_or_update(req):
        f = StatusForm(req.POST)

        if f.is_valid():
            _id = req.POST.get('id', None)
            if _id is None or _id == '':
                try:
                    # Replace the grant id with its object and save
                    # f.save(commit=False)
                    # f.grant = Grant.objects.get(pk=f.cleaned_data['grant'])
                    new_status = f.save()

                    # Redirect to the grant's detail view
                    # return populated_form(request, StatusForm(instance=new_status))
                    return refresh_grant_page(req, new_status.grant.id)

                except Grant.DoesNotExist:
                    return does_not_exist(f.grant, 'Grant')

            elif is_valid_id(_id):
                try:
                    s = Status.objects.get(pk=int(_id))

                    # Update each provided value on the row, then save it.
                    # Also, don't try to mutate the id or grant id of the row.
                    for field, value in f.cleaned_data.items():
                        if field != 'id' and field != 'pk' and field != 'grant':
                            setattr(s, field, value)
                    s.save()
                    return refresh_grant_page(req, s.grant.id)

                except Status.DoesNotExist:
                    # Return a 404 if the status id is valid but doesn't exist
                    return does_not_exist(_id, 'Status')

            else:
                # Return a 400 if the specified id is invalid
                return invalid_id()

        else:
            # Return a 400 if the form fails to validate
            return HttpResponse("Form data is invalid",
                                status=400)

    if request.method == 'GET':
        _id = request.GET.get('id', None)

        if _id is None or _id == '':
            # TODO: Set its grant attribute to one specified
            #       in the request and make it hidden. User
            #       shouldn't be manually specifying that.
            return blank_form(request)

        elif is_valid_id(_id):
            try:
                row = Status.objects.get(pk=_id)
                form = StatusForm(instance=row)
                return populated_form(request, form)

            except Status.DoesNotExist:
                return does_not_exist(_id, 'Status')

        else:
            return invalid_id()

    elif request.method == 'POST':
        # Either create or update the status, depending on if ID is given
        return create_or_update(request)

    else:
        # Return a 405
        return get_or_post_only()


def status_list(request):
    """Returns a list of all statuses--either for a specified grant, or in general."""
    template_path = 'sygma/partials/status-list.html'

    def render_response(req, rows):
        """Pull specified values from a queryset and render them in a template."""
        list_vals = [{"id": r.pk,
                      "status": r.status,
                      "details": r.details,
                      "amount": r.amount,
                      "date": r.updated_on} for r in rows]
        context = {
            "statuses": list_vals
        }
        #raise ValueError(context)
        return render(req, template_path, context)

    if request.method == 'GET':
        grant_id = request.GET.get('grant', None)

        if grant_id == '' or grant_id is None:
            # Given no id, return all statuses
            rows = Status.objects.all()
            return render_response(request, rows)

        elif is_valid_id(grant_id):
            # Return just the statuses for the specified grant
            grant_id = int(grant_id)
            rows = Status.objects.filter(grant__pk=grant_id)
            return render_response(request, rows)

        else:
            # Return a 400 if the specified id is invalid
            return invalid_id()

    else:
        return get_method_only()


def obligation(request):
    template_path = "sygma/obligation.html"

    def blank_form(req):
        # Render the template with a blank form
        context = {
            "form": ObligationForm(auto_id=True)
        }
        return render(req, template_path, context)

    def populated_form(req, f):
        context = {"form": f}
        return render(req, template_path, context)

    def refresh_grant_page(req, grant_id):
        # Refresh the Grant page with the updated Status
        # TODO: Preserve the user's filter and sort settings
        #       for the table of statuses (and obligations?)
        return redirect("/sygma/grant?id=" + str(grant_id))

    def create_or_update(req):
        f = ObligationForm(req.POST)

        if f.is_valid():
            _id = req.POST.get('id', None)
            if _id is None or _id == '':
                # Create record
                new_obligation = f.save()

                # Redirect to the grant's detail view
                return refresh_grant_page(req, new_obligation.grant.id)

            elif is_valid_id(_id):
                try:
                    o = Obligation.objects.get(pk=int(_id))

                    # Update each provided value on the row, then save it.
                    # Also, don't try to mutate the id or grant id of the row.
                    for field, value in f.cleaned_data.items():
                        if field != 'id' and field != 'pk' and field != 'grant':
                            setattr(o, field, value)
                    o.save()
                    return refresh_grant_page(req, o.grant.id)

                except Status.DoesNotExist:
                    # Return a 404 if the status id is valid but doesn't exist
                    return does_not_exist(_id, 'Obligation')

            else:
                # Return a 400 if the specified id is invalid
                return invalid_id()

        else:
            # Return a 400 if the form fails to validate
            return HttpResponse("Form data is invalid",
                                status=400)
    
    if request.method == 'GET':
        _id = request.GET.get('id', None)

        if _id is None or _id == '':
            # TODO: Set its grant attribute to one specified
            #       in the request and make it hidden. User
            #       shouldn't be manually specifying that.
            return blank_form(request)

        elif is_valid_id(_id):
            try:
                row = Obligation.objects.get(pk=_id)
                form = ObligationForm(instance=row)
                return populated_form(request, form)

            except Obligation.DoesNotExist:
                return does_not_exist(_id, 'Status')

        else:
            return invalid_id()
    elif request.method == 'POST':
        return create_or_update(request)
    else:
        return get_or_post_only()


def obligations_list(request):
    """Returns a list of all statuses--either for a specified grant, or in general."""
    template_path = 'sygma/partials/obligation-list.html'

    def render_response(req, rows):
        """Pull specified values from a queryset and render them in a template."""
        list_vals = [{"id": r.pk,
                      "title": r.title,
                      "details": r.details,
                      "due": r.due} for r in rows]
        context = {
            "obligations": list_vals
        }
        return render(req, template_path, context)

    if request.method == 'GET':
        grant_id = request.GET.get('grant', None)

        if grant_id == '' or grant_id is None:
            # Given no id, return all statuses
            rows = Obligation.objects.all()
            return render_response(request, rows)

        elif is_valid_id(grant_id):
            # Return just the statuses for the specified grant
            grant_id = int(grant_id)
            rows = Obligation.objects.filter(grant__pk=grant_id)
            return render_response(request, rows)

        else:
            # Return a 400 if the specified id is invalid
            return invalid_id()

    else:
        return get_method_only()