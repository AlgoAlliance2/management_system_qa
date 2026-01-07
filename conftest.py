import pytest
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv

# Load env variables from .env if present
load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override browser context arguments if needed.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }

@pytest.fixture
def auth_header():
    """
    Example fixture if you need to pass headers.
    """
    # You might want to get a token via API login here
    return {}
