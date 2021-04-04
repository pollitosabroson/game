import logging
from ast import literal_eval
from collections import OrderedDict

from assignment.models import AssignmentModel
from rest_framework import serializers

logger = logging.getLogger(__name__)
from rest_framework.fields import (  # NOQA # isort:skip
    CreateOnlyDefault, CurrentUserDefault, SkipField, empty
)


class ArraySerializer(serializers.Serializer):
    """ArraySerializer."""
    value = serializers.ListField()

    def save(self, **kwargs):
        """Override method save for transfor values"""
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        parse_value = list(
            AssignmentModel.parse_value(
                value_list=validated_data['value']
            )
        )
        depth_value = AssignmentModel.calculate_depth(validated_data['value'])
        return {
            'original': validated_data['value'],
            'content': parse_value,
            'depth': depth_value
        }


class StrSerializer(serializers.Serializer):
    """StrSerializer."""

    value = serializers.CharField(
        max_length=None,
        min_length=None
    )
    default_softspace = serializers.CharField(
        max_length=None,
        min_length=None,
        required=False,
        allow_blank=True,
        default=';'
    )

    def save(self, **kwargs):
        """Override method save for transfor values"""
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        value = literal_eval(
            validated_data['value'].replace(
                validated_data['default_softspace'], ','
            )
        )
        parse_value = tuple(
            AssignmentModel.parse_value(
                value_list=value
            )
        )
        depth_value = AssignmentModel.calculate_depth(value)
        return {
            'original': validated_data['value'],
            'content': str(parse_value).replace(
                ',', validated_data['default_softspace']
            ),
            'depth': depth_value
        }


class AssignmentSerializer(serializers.Serializer):
    """AssignmentSerializer."""

    content = serializers.CharField()
    created_date = serializers.DateTimeField()
    depth = serializers.IntegerField()
    last_modified = serializers.DateTimeField()
    original = serializers.CharField()
    time_execution = serializers.FloatField()
    type_input = serializers.CharField()

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        ret['original'] = instance.data.get('original')
        ret['content'] = instance.data.get('content')
        ret['depth'] = instance.data.get('depth')
        ret['time_execution'] = instance.data.get('time_execution')
        ret['type_input'] = instance.DICT_CHOICES.get(instance.type_input)
        ret['created_date'] = instance.created_date
        ret['last_modified'] = instance.last_modified
        return ret
