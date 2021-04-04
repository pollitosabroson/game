import logging

import coreapi
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters
from rest_framework.compat import coreschema

logger = logging.getLogger(__name__)


class TypeFilter(filters.BaseFilterBackend):
    """
    Filter for documentation purposes
    """

    NAME_FILTER = 'i_type'

    def get_schema_fields(self, view):
        schema_cls = coreschema.String
        fields = []

        fields += [
            coreapi.Field(
                name=self.NAME_FILTER,
                required=False,
                location='query',
                schema=schema_cls(
                    title=_('type of parse'),
                    description=_(
                        'Filter to get the results according to their type'
                    )
                ),
            )
        ]
        return fields

    def filter_queryset(self, request, queryset, view):
        """Filter values.
        Args:
            reques(Request): Request from view
            queryset(Queryset): Queryset where we are going to apply the filter
            view(View): View in which you are filtering
        Return:
            Queryset: Queryset with filtered data
        """
        value = request.GET.get(self.NAME_FILTER)
        if value:
            return queryset.filter(type_input=value)
        return queryset
