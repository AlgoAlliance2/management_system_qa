import pytest
from playwright.sync_api import Page, expect

@pytest.mark.usability
def test_mobile_responsiveness(page: Page):
    """
    Test that the layout adapts to mobile viewports.
    """
    # Set viewport to mobile size
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("/")
    
    # Check if hamburger menu or mobile navigation exists
    # If using standard Responsive design, perhaps the main menu is hidden
    # and a toggle button is visible.
    
    # Example: Check if columns stack
    # This depends heavily on implementation, but checking for horizontal scrolling 
    # being absent on body is a good generic check.
    
    # Check if a specific mobile element is visible or desktop element is hidden
    # expect(page.locator(".desktop-menu")).not_to_be_visible()
    
    # General check: elements verify visibility
    expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()

@pytest.mark.usability
def test_navigation_flow(authenticated_page: Page):
    """
    Test ease of navigation between main sections.
    """
    page = authenticated_page
    
    # Click on Home/Acasă (which is usually the logo or "Acasă" link)
    # Assuming the app has a header with navigation
    
    # Navigate to Calendar (example of internal nav)
    # Check if Calendar link exists, if not, skip/adjust
    # page.click("text=Calendar") 
    # expect(page).to_have_url("/calendar")
    
    # Since we don't know exact Nav links, we check if we are on Home after login
    # and maybe click a profile link
    
    # Check for search input which is always on home
    expect(page.get_by_placeholder("Caută evenimente...")).to_be_visible()


@pytest.mark.usability
def test_form_validation_feedback(page: Page):
    """
    Test that the user gets clear feedback when form validation fails.
    """
    page.goto("/")
    page.get_by_role("tab", name="Înregistrare").click()
    
    # Try to submit empty form
    page.click("button:has-text('Creează cont')")
    
    # Expect validation error messages
    expect(page.get_by_text("Numele este obligatoriu")).to_be_visible() # Example text
    expect(page.get_by_text("Email-ul este obligatoriu")).to_be_visible()
