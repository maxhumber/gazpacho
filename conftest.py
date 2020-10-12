from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def create_mock_responses():
    """Return a function that mocks urllib responses."""

    def _create_mocks(
        content,
        content_type="application/json",
        mock_path="gazpacho.http.get.build_opener",
    ):
        mock_opener = MagicMock()
        patch(mock_path, mock_opener).start()
        mock_response = MagicMock()
        mock_opener.open.return_value = content
        mock_opener.return_value.open.return_value.__enter__.return_value = (
            mock_response
        )
        mock_response.read.return_value.decode.return_value = content
        mock_response.headers.get_content_type.return_value = content_type
        return mock_opener, mock_response

    yield _create_mocks
    patch.stopall()
