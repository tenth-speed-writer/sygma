from django.http import HttpResponse
from django.core.serializers import serialize


def model_field_names(model_obj):
    """Returns a list of non-relational field names for a data model object."""
    field_slugs = [str(f) for f in model_obj._meta.get_fields(include_parents=False)]
    # They're in the format of app.Model.fieldname.
    # We'll also drop any relational fields.
    field_names = [f.split('.')[-1]
                   for f in field_slugs
                   if 'Rel:' not in f]
    return field_names


def dict_from_fields(d, fields):
    """Gets only the specified fields from a dict.
    Use with model_field_names to put a hard restriction on which model attributes
    are able to make it through the views layer."""
    res_dict = {}
    for f in fields:
        res_dict[f] = getattr(d, f, None)
    return res_dict


def dict_from_request(request, fields, verb="GET"):
    """Much like dict_from_fields, but for request data."""
    res_dict = {}
    for f in fields:
        res_dict[f] = getattr(request, verb).get(f, None)
    return res_dict


def is_valid_id(val):
    if isinstance(val, int):
        if val >= 0:
            return True
        else:
            return False
    elif isinstance(val, str):
        # Checks int-castability -and- at-least-zeroness
        return val.isdigit() and int(val) >= 0
    else:
        return False


def get_or_post_only():
    """Returns a 405 stating only GET and POST requests are accepted."""
    return HttpResponse("Unsupported method; use GET or POST.",
                        status=405)


def get_method_only():
    """Returns a 405 stating only GET requests are accepted."""
    return HttpResponse("Only GET requests are supported for this url.",
                        status=405)


def post_method_only():
    """Returns a 405 stating only post requests are accepted."""
    return HttpResponse("Only POST requests are supported for this url.",
                        status=405)


def return_rows(qs):
    # Serializes a queryset and returns it as a JSON response
    return HttpResponse(serialize('json', qs),
                        content_type='application/json',
                        status=200)


def does_not_exist(id, obj_name):
    """Returns a 404."""
    return HttpResponse('{} with id {} does not exist'.format(obj_name, str(id)),
                        status=404)


def invalid_id():
    """Returns an HTTP 400 response stating that the given .id is not a valid index value."""
    return HttpResponse('If given, id must be a valid index (an integer of at least zero.)',
                        status=400)


def update_row(row, **kwargs):
    """Updates a row with given keyword args, then saves it."""
    for column, value in kwargs.items():
        setattr(row, column, value)
    row.save()
    return row


US_STATES = [("AL", "Alabama"),
             ("AK", "Alaska"),
             ("AZ", "Arizona"),
             ("AR", "Arkansas"),
             ("CA", "California"),
             ("CO", "Colorado"),
             ("CT", "Connecticut"),
             ("DE", "Delaware"),
             ("FL", "Florida"),
             ("GA", "Georgia"),
             ("HI", "Hawaii"),
             ("ID", "Idaho"),
             ("IL", "Illinois"),
             ("IN", "Indiana"),
             ("IA", "Iowa"),
             ("KS", "Kansas"),
             ("KY", "Kentucky"),
             ("LA", "Louisiana"),
             ("ME", "Maine"),
             ("MD", "Maryland"),
             ("MA", "Massachusetts"),
             ("MI", "Michigan"),
             ("MN", "Minnesota"),
             ("MS", "Mississippi"),
             ("MO", "Missouri"),
             ("MT", "Montana"),
             ("NE", "Nebraska"),
             ("NV", "Nevada"),
             ("NH", "New Hampshire"),
             ("NJ", "New Jersey"),
             ("NM", "New Mexico"),
             ("NY", "New York"),
             ("NC", "North Carolina"),
             ("ND", "North Dakota"),
             ("OH", "Ohio"),
             ("OK", "Oklahoma"),
             ("OR", "Oregon"),
             ("PA", "Pennsylvania"),
             ("RI", "Rhode Island"),
             ("SC", "South Carolina"),
             ("SD", "South Dakota"),
             ("TN", "Tennessee"),
             ("UT", "Utah"),
             ("VT", "Vermont"),
             ("VA", "Virginia"),
             ("WA", "Washington"),
             ("WV", "West Virginia"),
             ("WI", "Wisconsin"),
             ("WY", "Wyoming")]