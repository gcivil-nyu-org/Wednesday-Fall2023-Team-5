from django import template

register = template.Library()
"""Custom template tags for DTL"""


@register.simple_tag(name="slice_list")
def slice_list(arr, start, end):
    return arr[start:end]


@register.simple_tag(name="get_by_index")
def get_by_index(arr, ind):
    print("Accessed")
    return arr[ind]
