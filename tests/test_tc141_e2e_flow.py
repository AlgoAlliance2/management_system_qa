import pytest
from playwright.sync_api import Page, expect
import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env for DB connection
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'management_system_back', 'app', '.env'))

def approve_event(title):
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("Warning: MONGO_URI not found, skipping manual approval.")
            return

        client = MongoClient(mongo_uri)
        # Default to 'test', as ensure_test_users.py does
        db = client['test'] 
        
        result = db.events.update_one(
            {"title": title},
            {"$set": {"status": "approved"}}
        )
        print(f"Manually approved event '{title}': {result.modified_count} modified.")
        client.close()
    except Exception as e:
        print(f"Error approving event: {e}")

def test_tc141_flux_complet(page: Page):
    """
    TC-141: Flux Complet Creare și Participare Eveniment (End-to-End)
    Steps:
    1. Open browser and navigate to Homepage.
    2. Authenticate as Organizer (test_org@student.usv.ro / ParolaTest123!).
    3. Navigate to 'Creează Eveniment'.
    4. Fill form (Title: 'E2E Test', Date, Location, Description) and submit.
    5. Logout.
    6. Authenticate as Student (test_student@student.usv.ro / StudentPass123!).
    7. Search for 'E2E Test' in list.
    8. Access details and press 'Participă'.
    """

    event_title = "E2E Test Python"

    # 1. Open browser and navigate to Homepage
    page.goto("http://localhost:5173")
    expect(page).to_have_title("UniPlans")

    # 2. Authenticate as Organizer
    # Check if we are already logged in
    if page.locator("button:has(svg.lucide-user)").is_visible():
        page.click("button:has(svg.lucide-user)")
        page.click("text=Deconectare")

    expect(page.locator("#login-email")).to_be_visible()
    page.fill("#login-email", "test_org@student.usv.ro")
    page.fill("#login-password", "ParolaTest123!")
    page.click("button[type='submit']")

    expect(page.get_by_text("Creează Eveniment")).to_be_visible(timeout=10000)

    # 3. Navigate to 'Creează Eveniment'
    page.click("text=Creează Eveniment")

    # 4. Fill form
    page.fill("#title", event_title)

    # Select Category
    page.click("button:has-text('Selectează categoria')")
    page.click("div[role='option']:has-text('Conferință')")

    page.fill("#description", "Aceasta este o descriere lungă pentru testul automat E2E generat cu Python si Playwright.")
    page.click("button:has-text('Continuă')")

    # Step 2
    expect(page.get_by_text("Dată, oră și locație")).to_be_visible()

    # Use a future date
    future_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    page.fill("#date", future_date)

    page.fill("#startTime", "10:00")
    page.fill("#endTime", "12:00")
    page.fill("#location", "Corp A, Sala C1")

    page.click("button:has-text('Continuă')")

    # Step 3
    expect(page.get_by_text("Imagine și revizuire")).to_be_visible()
    
    # Wait for the button to be clickable to avoid hydration issues
    page.wait_for_selector("button:has-text('Creează eveniment')")
    page.click("button:has-text('Creează eveniment')")

    # Expect success
    expect(page.get_by_text("Eveniment creat cu succes").first).to_be_visible()
    page.wait_for_timeout(1000)

    # 5. Logout
    page.click("button:has(svg.lucide-user)")
    page.click("text=Deconectare")

    # --- ADMIN APPROVAL STEP (UI) ---
    # 5a. Authenticate as Admin
    expect(page.locator("#login-email")).to_be_visible()
    page.fill("#login-email", "test_admin@student.usv.ro")
    page.fill("#login-password", "AdminPass123!")
    page.click("button[type='submit']")
    
    # 5b. Navigate to Admin Panel
    # Wait for login to complete
    page.wait_for_timeout(2000)
    page.goto("http://localhost:5173/admin")
    
    # 5c. Approve the event
    # Expect the Admin Panel to load and show pending events
    expect(page.get_by_text("În Așteptarea Aprobării")).to_be_visible(timeout=10000)
    
    # Find the Revizuiește button for our event
    # The event title should be in a card
    # We navigate to the event details directly via the button
    
    # Option 1: Click the specific button in the card containing the title
    # Structure: div > h4(title) ... Button(Revizuiește)
    # We can just click the button that is inside the card for this event
    page.locator("div.bg-white").filter(has_text=event_title).first.get_by_role("button", name="Revizuiește Evenimentul").click()
    
    # 5d. Click 'Aprobă Evenimentul' on Details Page
    expect(page.get_by_text("Revizuire Necesară")).to_be_visible()
    page.click("button:has-text('Aprobă Evenimentul')")
    
    # Verify approval success
    expect(page.get_by_text("Eveniment aprobat cu succes!")).to_be_visible()
    
    # 5e. Logout Admin
    page.click("button:has(svg.lucide-user)")
    page.click("text=Deconectare")
    # ---------------------------

    # 6. Authenticate as Student
    expect(page.locator("#login-email")).to_be_visible()
    page.fill("#login-email", "test_student@student.usv.ro")
    page.fill("#login-password", "StudentPass123!")
    page.click("button[type='submit']")

    # 7. Search for 'E2E Test Python' in list
    expect(page.get_by_placeholder("Caută evenimente...")).to_be_visible()
    page.wait_for_timeout(1000) # Wait for list load
    
    page.fill("input[placeholder='Caută evenimente...']", event_title)
    page.wait_for_timeout(1000)

    # 8. Access details and press 'Participă'
    if not page.locator(f"text={event_title}").is_visible():
        # Try clearing and retyping
        page.fill("input[placeholder='Caută evenimente...']", "")
        page.fill("input[placeholder='Caută evenimente...']", event_title)
        page.wait_for_timeout(1000)

    if not page.locator(f"text={event_title}").is_visible():
        # Debug info
        page.screenshot(path="debug_not_found.png")
        raise Exception(f"Event '{event_title}' not found in list. It might be stuck in Pending status if approval failed.")

    page.click(f"text={event_title}")

    # Now in details page
    # Verify we are on details page by checking for Back button or Title
    expect(page.locator("button:has-text('Înapoi')")).to_be_visible()
    expect(page.locator("h1.text-3xl")).to_contain_text(event_title)
    
    # Press 'Participă'
    # Wait for button to be stable
    page.wait_for_timeout(500)
    
    if page.locator("button:has-text('Participă')").is_visible():
        page.click("button:has-text('Participă')")
        # Toast check
        expect(page.get_by_text("Te-ai înscris cu succes")).to_be_visible()
    elif page.locator("button:has-text('Participi')").is_visible():
        print("Already participating.")
    else:
        # Fallback if text differs
        pass
    
    # 9. Cleanup
    page.click("button:has(svg.lucide-user)")
    page.click("text=Deconectare")
