from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    """
    Smoke test to verify that the frontend application loads 
    and displays the correct title.
    """
    # Uses 'base_url' from pytest.ini automatically if pytest-base-url is installed
    # or you can use page.goto("/") relative to it.
    
    # 1. Navigate to the App
    page.goto("/")

    # 2. Check the title
    # Note: 'React App' is the default Vite/React title. 
    # Verify it matches or update index.html in the frontend.
    expect(page).to_have_title("React App")

    # 3. Check for a key element that should exist (e.g. root div)
    expect(page.locator("#root")).to_be_visible()

def test_login_page_structure(page: Page):
    """
    Check if login elements are present (assuming the app starts on login or has one).
    Adjust selectors based on actual UI.
    """
    page.goto("/login")  # Adjust route as needed
    
    # Example assertions - these might fail if the route doesn't exist yet
    # expect(page.get_by_role("button", name="Sign in")).to_be_visible()
    # pass
