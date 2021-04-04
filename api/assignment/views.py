import logging
import time

from assignment.filters import TypeFilter
from django.utils.text import slugify
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .models import AssignmentModel
from .serializer import ArraySerializer, AssignmentSerializer, StrSerializer

logger = logging.getLogger(__name__)


class baseView(CreateAPIView):
    """Base view for parse and save values."""

    queryset = []
    permission_classes = []

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        start_time = time.time()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        value.update(
            {
                'time_execution': f"{(time.time() - start_time)}"
            }
        )
        try:
            AssignmentModel.new(
                data=value,
                type_input=self.type_parse
            )
            return Response(
                value,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                error={
                    'error': (
                        'we had problems with the transformation'
                        ' and storage of the values'
                    ),
                    'type': e
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        return serializer.save()


class CalculateAssignmentView(baseView):
    """View for parse and save values from array."""

    type_parse = AssignmentModel.ID_JSON
    serializer_class = ArraySerializer


class CalculateAssignmentStrView(baseView):
    """View for parse and save values from array."""

    serializer_class = StrSerializer
    type_parse = AssignmentModel.ID_STR


class EnvsView(ListAPIView):
    """Show visible envs."""

    permission_classes = []

    def list(self, request, *args, **kwargs):
        data = {}
        for k, v in AssignmentModel.DICT_CHOICES.items():
            data.update({
                slugify(v): {
                    'id': k,
                    'name': v,
                    'slug': slugify(v)
                }
            })
        return Response(data)

    def get_queryset(self):
        return []


class ListAssignmentView(ListAPIView):
    """Show all results that were parsed successfully.
    * To filter by type of parse you can check the IDs in the endpoint
    * /api/v1/envs
    """

    queryset = AssignmentModel.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [TypeFilter, ]
