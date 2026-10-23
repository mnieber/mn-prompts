from rest_framework.exceptions import ValidationError


def apply_filter_set_or_400(qs, filter_set_class, params):
    filter_set = filter_set_class(params, queryset=qs)
    if filter_set.is_valid():
        return filter_set.qs
    raise ValidationError(filter_set.errors)
