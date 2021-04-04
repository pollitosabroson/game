# -*- coding: utf-8 -*-
from assignment import views
from django.urls import path

app_name = 'assignments'
urlpatterns = [
    path(
        'parse-from-list',
        views.CalculateAssignmentView.as_view(),
        name='parse-from-list'
    ),
    path(
        'parse-from-str',
        views.CalculateAssignmentStrView.as_view(),
        name='parse-from-str'
    ),
    path(
        'envs',
        views.EnvsView.as_view(),
        name='envs'
    ),
    path(
        '',
        views.ListAssignmentView.as_view(),
        name='list-values'
    ),
]
