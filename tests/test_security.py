import pytest
from playwright.sync_api import Page, expect

@pytest.mark.security
def test_xss_in_comments(organizer_page: Page):
    """
    Test for XSS vulnerability in event comments/description.
    """
    page = organizer_page
    
    # Prerequisite: We need an event to comment on. Create one quickly.
    create_btn = page.locator("button:has-text('Creează Eveniment')")
    if create_btn.is_visible():
        create_btn.click()
    else:
        # Fallback manual navigation
        if "/create-event" not in page.url:
             page.goto("/create-event")

    # Fill form
    page.fill("#title", "XSS Test Event")
    page.click("text=Selectează categoria")
    
    # Robust Wait + Click for select
    page.locator("div[role='option']:has-text('Conferință')").click()
    
    page.fill("#description", "Safe description for security test. Meets length requirements (50 chars).")
    
    # Step 1 -> 2
    page.click("button:has-text('Continuă')")
    
    # Step 2
    page.fill("#date", "2025-01-01")
    page.fill("#time", "12:00")
    page.fill("#location", "Internet")
    page.fill("#maxAttendees", "10")
    
    # Step 2 -> 3
    page.click("button:has-text('Continuă')")
        
    page.click("button:has-text('Creează eveniment')")
    expect(page.get_by_text("Eveniment creat cu succes")).to_be_visible()

    # Go to an event (the one we just created should be on homepage or we are redirected there?)
    # Assuming redirect to organizer panel where event is listed
    # Click on the event details.
    
    # Wait for the event to appear in the list (if we are on organizer panel)
    # The organized events are listed. We need to click "Vezi Detalii" or finding the card.
    
    # Or go to '/' and find it.
    page.goto("/")
    page.wait_for_timeout(1000) # Give time to load
    
    # Click the first "Detalii" button found, assuming it's the latest event or one of them.
    # We might need to handle empty states, but we just created one.
    details_btn = page.locator("button:has-text('Detalii')").first
    expect(details_btn).to_be_visible()
    details_btn.click()
    
    # Try to post a malicious comment
    xss_payload = "<script>alert('XSS')</script>"
    page.fill("textarea", xss_payload) # Use generic textarea as there is only one usually
    page.click("button:has-text('Trimite comentariu')")
    
    # Reload page
    page.reload()
    
    # Check if the script executed (Playwright handles dialogs automtically, so we check if text is rendered as text, not HTML)
    # The comment should appear as text, not be executed.
    # Use .first in case multiple tests left multiple comments
    expect(page.get_by_text(xss_payload).first).to_be_visible()
    # Ensure no alert was triggered (handled by page.on('dialog'))

@pytest.mark.security
def test_protected_routes_access(page: Page):
    """
    Test that users cannot access protected routes without logging in.
    """
    page.goto("/admin") # Assuming /admin is protected
    
    # Should be redirected to login or home
    # Check if Login form is visible (AuthForm) by checking for unique Label or Tab
    expect(page.get_by_label("Email universitar")).to_be_visible()

@pytest.mark.security
def test_sql_injection_attempt_login(page: Page):
    """
    Basic SQL Injection attempt on login form.
    """
    page.goto("/")
    if page.get_by_role("tab", name="Autentificare").is_visible():
        page.get_by_role("tab", name="Autentificare").click()
    
    # Classic SQL injection payloads
    payloads = ["' OR '1'='1", "admin' --", "' OR 1=1 --"]
    
    for payload in payloads:
        # Fill email in active tab
        page.locator("div[role='tabpanel'][data-state='active'] input[type='email']").fill(payload)
        page.locator("div[role='tabpanel'][data-state='active'] input[type='password']").fill("password")
        
        page.click("button:has-text('Autentificare')")
        
        # Should fail authentication
        # Check if we are still on the login page (Login tab is visible) or an error appeared
        # Don't strictly expect a toast if it's flaky, but expect NOT to be redirected to home with user profile
        expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()

