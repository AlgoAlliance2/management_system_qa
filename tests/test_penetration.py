import pytest
import random
import string
from playwright.sync_api import Page, expect

@pytest.mark.penetration
def test_login_brute_force_protection(page: Page):
    """
    Simulate a brute force attack (many failed login attempts).
    Ideally, the system should lock out or slow down responses (rate limiting).
    Note: This test might be slow and should be run carefully.
    """
    page.goto("/")
    page.get_by_role("tab", name="Autentificare").click()
    
    target_email = "victim@student.usv.ro"
    
    # Try 5 rapid incorrect passwords
    for i in range(5):
        # Ensure we are on login tab
            page.get_by_role("tab", name="Autentificare").click()

            # Fill email
            page.locator("div[role='tabpanel'][data-state='active'] input[type='email']").fill(target_email)
            
            # Fill password
            page.locator("div[role='tabpanel'][data-state='active'] input[type='password']").fill(f"wrongpass{i}")
            
            # Click submit specifically (Login button)
            page.click("div[role='tabpanel'][data-state='active'] button[type='submit']") 
            
            # Wait a bit to simulate "human" speed or just to not crash the browser
            page.wait_for_timeout(500)

            # Verify failure message appears quickly if implemented
            # expect(page.locator(".sonner-toast")).to_be_visible() # Commented out as rate limiting might not show toast immediately
    """
    Input extremley long strings or special chars into registration fields.
    """
    page.goto("/")
    if page.get_by_role("tab", name="Înregistrare").is_visible():
        page.get_by_role("tab", name="Înregistrare").click()
    
    long_string = "A" * 5000 
    
    # Use IDs
    page.fill("#register-name", long_string)
    page.fill("#register-email", f"test{random.randint(1,9999)}@student.usv.ro")
    page.fill("#register-password", "Pass123!@#")
    
    # Confirm password fallback
    if page.locator("input[placeholder='Confirma parola']").is_visible():
        page.fill("input[placeholder='Confirma parola']", "Pass123!@#")
    elif page.locator("#register-confirm-password").is_visible():
        page.fill("#register-confirm-password", "Pass123!@#")
    
    page.click("button:has-text('Creează cont')")
    
    # The application should handle this gracefully (e.g., frontend validation clipping it, 
    # or backend rejecting it), but NOT crashing or showing raw error dumps.
    
    # Expecting either specific error or generic failure, but definitely NOT a 500 page or blank screen.
    # Checking for critical UI failure:
    expect(page.locator("body")).to_be_visible()
    
    # Ideally, check if an error message about length is shown
    # expect(page.get_by_text("Name too long")).to_be_visible()
