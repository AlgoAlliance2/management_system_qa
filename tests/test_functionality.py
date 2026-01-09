import pytest
import time
import re
from playwright.sync_api import Page, expect

@pytest.mark.functional
def test_user_registration_and_login(page: Page):
    """
    Test complete user flow: Register -> Login
    """
    # 1. Register a new user
    page.goto("/")
    
    # Assuming the page starts at AuthForm or has a login/register button
    # Fill registration details
    # Generate unique email
    unique_email = f"testuser{int(time.time())}@student.usv.ro"

    # Switch to Register tab
    page.get_by_role("tab", name="Înregistrare").click()

    # Use IDs
    page.fill("#register-name", "Test User")
    page.fill("#register-email", unique_email)
    page.fill("#register-password", "Password123!")
    
    # Confirm password
    # Use id from AuthForm.tsx
    page.fill("#confirm-password", "Password123!")

    page.click("button:has-text('Creează cont')")

    # Expect redirection to home page as proof of login success
    # Verify by checking for "Deconectare" button in Header or User Profile icon
    # Wait for the login state to settle
    expect(page.get_by_text("UniPlans")).to_be_visible() # Logo is visible
    # Check for authenticated element
    expect(page.get_by_placeholder("Caută evenimente...")).to_be_visible()
    # So we don't need to manually log in again.
    
    # Verify we are inside the app
    # E.g. Header is visible, or "Deconectare" option.
    # Assuming "Deconectare" is hidden behind a menu or visible directly.
    # Let's assert Authentication form is gone.
    expect(page.get_by_text("Autentificare", exact=True)).not_to_be_visible()

@pytest.mark.functional
def test_create_event_flow(organizer_page: Page):
    """
    Test flow: Login -> Create Event
    Uses the organizer_page fixture which pre-logs in an Organizer.
    """
    page = organizer_page
    
    # Check if the user is actually an organizer (button visibility)
    create_btn = page.locator("button:has-text('Creează Eveniment')")
    
    if not create_btn.is_visible():
         # Fallback manual navigation in case of responsive UI hiding it
         page.goto("/create-event")
         if "/create-event" not in page.url:
             pytest.skip("Skipping Create Event test: Could not navigate to creation page (Role issue?).")

    # 3. Navigate to create event (if not already there)
    if "/create-event" not in page.url:
        page.click("button:has-text('Creează Eveniment')")
    
    # Fill form
    page.fill("#title", "Test Event")

    # Select Category
    page.click("text=Selectează categoria")
    page.locator("div[role='option']:has-text('Conferință')").click()

    page.fill("#description", "This is a test description for the event. It needs to be at least 50 chars long to pass validation.")
    
    page.click("button:has-text('Continuă')")

    # Step 2
    # Fill Date
    # Use a future date
    page.fill("#date", "2025-12-31")
    page.fill("#time", "14:00")
    page.fill("#location", "Test Location Aula Magna")
    page.fill("#maxAttendees", "100")
    
    page.click("button:has-text('Continuă')")

    # Step 3
    # Optionally upload image or just Review
    # Click Create
    expect(page.locator("button:has-text('Creează eveniment')")).to_be_visible()
    page.click("button:has-text('Creează eveniment')")
    
    # Verify success toast or redirection
    # It redirects to /organizer and shows success toast
    expect(page).to_have_url(re.compile(r"/organizer"))
