from django import forms
from .util import US_STATES
from .models import Grantmaker, Grant, Status, Obligation


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class GrantmakerForm(forms.ModelForm):
    class Meta:
        model = Grantmaker
        fields = ['id', 'name', 'kind', 'description', 'mission',
                  'address', 'address2', 'city', 'state', 'zip_code',
                  'country', 'email', 'url', 'phone', 'extension']
    id = forms.IntegerField(required=False,
                            widget=forms.HiddenInput)
    name = forms.CharField()
    kind = forms.ChoiceField(choices=(("OPEN", "Open"),
                                      ("PRIVATE", "Private"),
                                      ("GOVT", "Government")),
                             label="Kind",
                             widget=forms.Select)
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)
    mission = forms.CharField(required=False,
                              widget=forms.Textarea)
    address = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.ChoiceField(label="State",
                              required=False,
                              widget=forms.Select)
    zip_code = forms.CharField(required=False)
    country = forms.CharField(required=False)
    email = forms.CharField(required=False)
    url = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    extension = forms.CharField(required=False)


class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = ['id', 'grantmaker', 'name', 'description',
                  'deadline', 'restricted', 'restrictions']

    class GrantGrantmakerModelChoiceField(forms.ModelChoiceField):
        """Method called by Django which determines how each relational choice is labeled
        Borrowed from https://www.webforefront.com/django/modelformrelationships.html."""
        def label_from_instance(self, obj):
            return obj.name

    # # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    # # Credit for this method of putting potential reference objects in a selection field.
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     grantmakers = Grantmaker.objects.all().order_by('name')
    #     self.fields['grantmaker'].queryset = grantmakers
    id = forms.IntegerField(required=False,
                            widget=forms.HiddenInput)
    grantmaker = GrantGrantmakerModelChoiceField(queryset=Grantmaker.objects.all())
    name = forms.CharField()
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)
    deadline = forms.DateField(required=False,
                               widget=forms.SelectDateWidget)
    restricted = forms.ChoiceField(required=True,
                                   choices=[("YES", "Restricted"),
                                            ("NO", "Unrestricted"),
                                            ("UNK", "Unknown")],
                                   widget=forms.Select)
    restrictions = forms.CharField(required=False,
                                   widget=forms.Textarea)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['id', 'grant', 'status', 'amount', 'details']

    class StatusGrantModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.name

    id = forms.IntegerField(required=False,
                            widget=forms.HiddenInput)
    grant = StatusGrantModelChoiceField(queryset=Grant.objects.all())
    status = forms.ChoiceField(choices=[("LOISENT", "Letter of Intent Sent"),
                                        ("LOIACCEPTED", "Letter of Intent Accepted"),
                                        ("INPROGRESS", "Application in progress"),
                                        ("SUBMITTED", "Submitted"),
                                        ("REJECTED", "Rejected"),
                                        ("OFFERED", "Offered"),
                                        ("ACCEPTED", "Accepted"),
                                        ("RECEIVED", "Received")])
    amount = forms.DecimalField(decimal_places=2,
                                required=False)
    details = forms.CharField(required=False,
                              widget=forms.Textarea)


class ObligationForm(forms.ModelForm):
    class Meta:
        model = Obligation
        fields = ['id', 'grant', 'due', 'title', 'details', 'fulfilled']

    class ObligationGrantModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.name

    id = forms.IntegerField(required=False,
                            widget=forms.HiddenInput)
    grant = ObligationGrantModelChoiceField(queryset=Grant.objects.all())
    details = forms.CharField(required=False,
                              widget=forms.Textarea)
    title = forms.CharField(max_length=250)
    due = forms.DateField(widget=forms.SelectDateWidget)
    fulfilled = forms.BooleanField(required=False)