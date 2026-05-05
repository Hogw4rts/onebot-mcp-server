"""Shared test fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def base_url() -> str:
    return "http://test-taffy:5801"


@pytest.fixture
def api_key() -> str:
    return "test-api-key-12345"