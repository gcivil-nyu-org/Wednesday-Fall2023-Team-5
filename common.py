# ------- Creating new class of array field using postgres.fields -------
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=...,
                                                    choices=(...,)),
                                   default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,  # remove this for list selection
        }
        defaults.update(kwargs)

        return super(ArrayField, self).formfield(**defaults)


# ----------------------------------------------------------------------
def retrieve_none_or_403(
    request, target_model, identifier, message="You are not allowed to edit this."
):
    try:
        instance = target_model.objects.get(id=identifier)
        if instance.user != request.user:
            messages.warning(request, message)
            raise PermissionDenied
    except ObjectDoesNotExist:
        instance = None

    return instance
