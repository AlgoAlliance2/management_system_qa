import pytest
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv

# Load env variables from backend .env
load_dotenv(dotenv_path="../management_system_back/app/.env")

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
    # Placeholder if API tests need headers
    return {}

@pytest.fixture
def test_user_creds():
    return {
        "email": os.getenv("TEST_USER_EMAIL"),
        "password": os.getenv("TEST_USER_PASSWORD")
    }

@pytest.fixture
def organizer_creds():
    return {
        "email": os.getenv("TEST_ORG_EMAIL"),
        "password": os.getenv("TEST_ORG_PASSWORD")
    }

@pytest.fixture
def admin_creds():
    return {
        "email": os.getenv("TEST_ADMIN_EMAIL"),
        "password": os.getenv("TEST_ADMIN_PASSWORD")
    }

@pytest.fixture
def student_creds():
    return {
        "email": os.getenv("TEST_STUDENT_EMAIL"),
        "password": os.getenv("TEST_STUDENT_PASSWORD")
    }

def perform_login(page: Page, user_creds):
    page.goto("/")
    
    # 1. Check if already logged in and Logout if needed to switch users
    # Simplest strategy: Always logout if someone is logged in
    try:
        if page.locator("button:has(.lucide-user)").is_visible():
            page.locator("button:has(.lucide-user)").click()
            # Wait for dropdown
            if page.get_by_text("Deconectare").is_visible():
                page.get_by_text("Deconectare").click()
                expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()
            else:
                # If dropdown failed to open or something
                page.reload()
    except:
        pass # maybe it was not visible

    # Perform Login
    if page.get_by_role("tab", name="Autentificare").is_visible():
        page.get_by_role("tab", name="Autentificare").click()
    
    # Ensure panel is active
    login_panel = page.locator("div[role='tabpanel'][data-state='active']")
    # If no panel found (maybe tabs are different), try body
    if login_panel.count() == 0: 
        login_panel = page.locator("body")

    # Fill Email
    if login_panel.locator("#login-email").count() > 0:
         login_panel.locator("#login-email").fill(user_creds["email"])
    elif login_panel.locator("input[type='email']").count() > 0:
         login_panel.locator("input[type='email']").first.fill(user_creds["email"])
    
    # Fill Password
    if login_panel.locator("#login-password").count() > 0:
         login_panel.locator("#login-password").fill(user_creds["password"])
    elif login_panel.locator("input[type='password']").count() > 0:
         login_panel.locator("input[type='password']").first.fill(user_creds["password"])
    
    # Submit
    if login_panel.locator("button[type='submit']").count() > 0:
        login_panel.locator("button[type='submit']").click()
    else:
        # Sometimes tab switch is slow or selectors are ambiguous
        page.locator("button:has-text('Autentificare')").click()
    
    # Verify Login
    # Wait for User Avatar/Menu
    try:
        expect(page.locator("button:has(.lucide-user)")).to_be_visible(timeout=10000)
    except:
        # Debugging Login Failure
        print(f"DEBUG: Login failed for {user_creds['email']}. Page Content:\n{page.content()[:500]}")
        raise
    
    return page

@pytest.fixture
def authenticated_page(page: Page, test_user_creds):
    return perform_login(page, test_user_creds)

@pytest.fixture
def organizer_page(page: Page, organizer_creds):
    return perform_login(page, organizer_creds)

@pytest.fixture
def admin_page(page: Page, admin_creds):
    return perform_login(page, admin_creds)

@pytest.fixture
def student_page(page: Page, student_creds):
    return perform_login(page, student_creds)

    """
    Example fixture if you need to pass headers.
    """
    # You might want to get a token via API login here
    return {}
