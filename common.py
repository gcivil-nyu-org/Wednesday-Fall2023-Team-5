# ------- Creating new class of array field using postgres.fields -------
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import ArrayField
from django import forms


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
