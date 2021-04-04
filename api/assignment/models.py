from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class AssignmentModel(models.Model):

    ID_JSON = 10
    TYPE_JSON = 'Json'
    ID_STR = 20
    TYPE_STR = 'String'

    DICT_CHOICES = {
        ID_JSON: TYPE_JSON,
        ID_STR: TYPE_STR
    }

    Choices = [
        (ID_JSON, TYPE_JSON),
        (ID_STR, TYPE_STR),
    ]

    data = JSONField(
        default=dict
    )
    type_input = models.IntegerField(
        choices=Choices
    )
    created_date = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now_add=True,
        verbose_name=_('created date')
    )
    last_modified = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now=True,
        verbose_name=_('last modified'),
    )

    @classmethod
    def new(cls, data=None, type_input=ID_JSON):
        """Add new value for bbdd.
        Args:
            data(Dict): Dict with values to save
            type_input(int): type value to create
        Return:
            Instance: Return new instance create
        """
        i_data = data or {}
        assignment = cls(
            data=i_data,
            type_input=type_input
        )
        assignment.save()
        return assignment

    @classmethod
    def parse_value(cls, value_list=None, tree_types=(list, tuple)):
        """.
        Args:
            value_list(list, Optional): list of value to parse
            tree_types(tuple, Optional): values to validate
        return:
            Yield: value to valdiation
        """

        if isinstance(value_list, tree_types):
            for value in value_list:
                for subvalue in cls.parse_value(value, tree_types):
                    yield subvalue
        else:
            yield value_list

    @classmethod
    def calculate_depth(cls, values, tree_types=(list, tuple), count=None):
        iter_value = 0
        i_count = count or []
        for value in values:
            if isinstance(value, tree_types):
                iter_value += 1
                i_count.append(iter_value)
                return cls.calculate_depth(value, tree_types, i_count)
        return len(i_count)
