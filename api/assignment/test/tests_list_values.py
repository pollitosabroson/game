import logging

import pytest
from core.utils import parse_response_content
from django.urls import reverse
from rest_framework import status

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('tangelo.urls')
class TestValidateStr:
    """Specific tests for validation values in list."""

    url = reverse('assignments:list-values')
    @staticmethod
    def get_success_fixtures():
        """values list for cases where the endpoint
        have an answer success
        """
        return [
            {}
        ]

    def make_post_request(self, client, params=None, **kwargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or {}
        response = client.get(
            self.url,
            i_params,
            **headers
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        for fixtures in self.get_success_fixtures():
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_200_OK == response_status
