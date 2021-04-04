import json
import logging

import pytest
from assignment.schemas import conf_schema_response_str
from core.utils import parse_response_content
from django.urls import reverse
from rest_framework import status

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('tangelo.urls')
class TestValidateStr:
    """Specific tests for validation values in list."""

    url = reverse('assignments:parse-from-str')
    @staticmethod
    def get_success_fixtures():
        """values list for cases where the endpoint
        have an answer success
        """
        return [
            {
                'value': '((10 ; 20 ; 30) ; 40)',
                'validation': {
                    'content': '(10; 20; 30; 40)',
                }
            },
            {
                'value': "(('A' ; 20 ; ('B')) ; 40)",
                'validation': {
                    'content': "('A'; 20; 'B'; 40)",
                }
            },
            {
                'value': "((10 ; ((20 ; (30))) ; (40)))",
                'validation': {
                    'content': '(10; 20; 30; 40)'
                }
            },
            {
                'value': "('♣' ; '♦' ; '♥')",
                'validation': {
                    'content': "('♣'; '♦'; '♥')",
                }
            },
        ]

    @staticmethod
    def get_bad_request_fixtures():
        """User list for cases where the endpoint
        have a fail answer
        """
        return [
            {
                'value': {}
            },
            {},
        ]

    def make_post_request(self, client, params=None, **kwargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or {}
        body = {}
        body.update(**i_params)
        body = json.dumps(body)
        response = client.post(
            self.url,
            body,
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
            assert conf_schema_response_str.validate(response_content)
            assert status.HTTP_201_CREATED == response_status
            self.validation(response_content, fixtures['validation'])

    def test_bad_request(self, client):
        """Test to validate that a user cannot be edited."""
        for fixtures in self.get_bad_request_fixtures():
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_400_BAD_REQUEST == response_status

    @staticmethod
    def validation(content, validation):
        """Validate value."""
        for key in validation.keys():
            assert content[key] == validation[key]
