import sys
from unittest.mock import MagicMock, patch

import pytest

from gazpacho.get import get


@pytest.fixture
def create_mock_responses():
    """Return a function that mocks urllib responses."""

    def _create_mocks(
        content,
        content_type="application/json",
        mock_module=sys.modules[get.__module__],
        mock_func="build_opener",
    ):
        mock_opener_patch = patch.object(mock_module, mock_func)
        mock_opener = mock_opener_patch.start()
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
