import pytest
from playwright.sync_api import Page, expect
import os
import socket
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

def find_active_backend_port():
    """
    Flexibly find the port where the backend is running.
    """
    candidates = [8080, 3000, 3001, 5000]
    env_port = os.getenv("PORT")
    if env_port:
        try:
            candidates.insert(0, int(env_port))
        except ValueError:
            pass
    
    candidates = list(dict.fromkeys(candidates)) # Deduplicate

    print(f"DEBUG: Checking ports for active backend: {candidates}")
    for port in candidates:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(('localhost', port)) == 0:
                print(f"DEBUG: Found active backend on port {port}")
                return port
    return 8080

@pytest.fixture(autouse=True)
def api_proxy(page: Page):
    """
    Redirect frontend API calls to the actual backend URL.
    """
    backend_port = find_active_backend_port()
    backend_host = "http://localhost"
    backend_url = f"{backend_host}:{backend_port}"
    
    def handle_route(route):
        url = route.request.url
        # Redirect if request targets /api/ but not the detected backend port
        if "/api/" in url and f":{backend_port}" not in url:
            try:
                parts = url.split("/api/", 1)
                if len(parts) == 2:
                    new_url = f"{backend_url}/api/{parts[1]}"
                    route.continue_(url=new_url)
                    return
            except Exception:
                pass
        
        route.continue_()

    # Intercept all requests containing /api/
    page.route("**/api/**", handle_route)

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
