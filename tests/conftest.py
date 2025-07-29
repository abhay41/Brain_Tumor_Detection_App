# tests/conftest.py
import pytest
import os
import tempfile

@pytest.fixture
def app():
    from app.create_app import create_app
    app = create_app('testing')
    return app

@pytest.fixture
def test_client(app):
    return app.test_client()