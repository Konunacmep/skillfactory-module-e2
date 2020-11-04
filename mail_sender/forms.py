from django.forms import Form, ValidationError, CharField, IntegerField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EmailValidator, EMPTY_VALUES
from django.forms.fields import Field
from django.forms.widgets import TextInput, Textarea

class CommaSeparatedEmailField(Field):
    description = _(u"E-mail address(es)")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise ValidationError(_(u"This field is required."))

        for email in value:
            if not EmailValidator(email):
                raise ValidationError(_(u"'%s' is not a valid "
                                              "e-mail address.") % email)
        return value


class MailForm(Form):
    to = CommaSeparatedEmailField(required=True, widget=TextInput(attrs={'placeholder': 'Input Email', 'class': 'form-control'}))
    subject = CharField(initial='Default subject', widget=TextInput(attrs={'class': 'form-control'}))
    body = CharField(initial='Default body', widget=Textarea(attrs={'cols': '40', 'rows': '5', 'class': 'form-control'}))
    seconds = IntegerField(initial=10, widget=TextInput(attrs={'type': 'number', 'min': '0', 'class': 'form-control'}))

