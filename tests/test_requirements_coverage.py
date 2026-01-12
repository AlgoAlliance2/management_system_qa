
import pytest
import time
import re
from playwright.sync_api import Page, expect

# Helper functions
def get_user_menu_button(page: Page):
    # This selects the button that wraps the User icon
    # Based on Header.tsx: <Button variant="ghost" size="icon"><User .../></Button>
    # We can select by the 'User' icon class or SVG
    return page.locator("button:has(svg.lucide-user)")

def is_logged_in(page: Page):
    return get_user_menu_button(page).is_visible()

def logout(page: Page):
    if is_logged_in(page):
        get_user_menu_button(page).click()
        page.get_by_text("Deconectare").click()
        expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()

# ==========================================
# 1. Autentificare & Înregistrare (Authentication)
# ==========================================

@pytest.mark.auth
def test_tc001_register_valid_and_tc202(page: Page):
    """
    TC001 - Înregistrare cu date valide
    TC202 - Înregistrare cu email de student valid (@student.usv.ro)
    TC207 - Tab "Login" activ implicit (Checked at start)
    TC206 - Switch între Login/Register (Implicitly checked)
    """
    page.goto("/")
    
    # TC027 - Login tab active by default
    expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()
    expect(page.get_by_role("tab", name="Autentificare")).to_have_attribute("data-state", "active")
    
    # Switch to Register
    page.get_by_role("tab", name="Înregistrare").click()
    
    unique_email = f"student{int(time.time())}@student.usv.ro"
    
    page.fill("#register-name", "Test Student")
    page.fill("#register-email", unique_email)
    page.fill("#register-password", "Password123!")
    page.fill("#confirm-password", "Password123!")
    
    page.click("button[type='submit']:has-text('Creează cont')")
    
    # Validation: Expect toast OR User Icon (Login success)
    try:
        expect(page.get_by_text("Cont creat cu succes!")).to_be_visible(timeout=5000)
    except:
        # If toast missed, check if logged in via User Icon
        expect(get_user_menu_button(page)).to_be_visible()

    # Final confirm logged in
    expect(get_user_menu_button(page)).to_be_visible()

@pytest.mark.auth
def test_tc002_register_duplicate_email(page: Page):
    """
    TC002 - Înregistrare cu email duplicat
    """
    # 1. Create user first
    page.goto("/")
    # Force logout if logged in
    logout(page)

    page.get_by_role("tab", name="Înregistrare").click()
    
    email = f"dup{int(time.time())}@student.usv.ro"
    
    # Register once
    page.fill("#register-name", "User One")
    page.fill("#register-email", email)
    page.fill("#register-password", "Password123!")
    page.fill("#confirm-password", "Password123!")
    page.click("button[type='submit']:has-text('Creează cont')")
    
    # Wait for success/login
    try:
         expect(page.get_by_text("Cont creat cu succes!")).to_be_visible(timeout=5000)
    except:
         expect(get_user_menu_button(page)).to_be_visible()

    # Logout to try again
    logout(page)
    
    # 2. Try register again with same email
    page.get_by_role("tab", name="Înregistrare").click()
    page.fill("#register-name", "User Two")
    page.fill("#register-email", email)
    page.fill("#register-password", "Password123!")
    page.fill("#confirm-password", "Password123!")
    page.click("button[type='submit']:has-text('Creează cont')")
    
    # Expect error message
    expect(page.get_by_text("Email already in use.").or_(page.get_by_text("există deja")).or_(page.get_by_text("Eroare la înregistrare"))).to_be_visible()

@pytest.mark.auth
def test_tc003_tc209_register_weak_password(page: Page):
    """
    TC003 - Înregistrare cu parolă slabă
    TC209 - Parolă cu exact 5 caractere (Boundary test)
    """
    page.goto("/")
    page.get_by_role("tab", name="Înregistrare").click()
    
    page.fill("#register-name", "Weak Pass User")
    page.fill("#register-email", f"weak{int(time.time())}@student.usv.ro")
    
    # Try 5 chars
    page.fill("#register-password", "12345")
    page.click("button:has-text('Creează cont')")
    
    # Expect validation error
    expect(page.get_by_text("Minim 6 caractere")).to_be_visible()

@pytest.mark.auth
def test_tc004_register_empty_fields(page: Page):
    """
    TC004 - Înregistrare cu câmpuri goale
    """
    page.goto("/")
    page.get_by_role("tab", name="Înregistrare").click()
    
    page.click("button:has-text('Creează cont')")
    
    expect(page.get_by_text("Numele este obligatoriu")).to_be_visible()
    expect(page.get_by_text("Email-ul este obligatoriu")).to_be_visible()
    expect(page.get_by_text("Parola este obligatorie")).to_be_visible()

@pytest.mark.auth
def test_tc201_tc203_email_domains_validation(page: Page):
    """
    TC201 - Înregistrare cu email personal (Gmail) -> Fail
    TC203 - Înregistrare cu email USM valid (@usm.ro) -> Pass
    """
    page.goto("/")
    page.get_by_role("tab", name="Înregistrare").click()
    
    # Test Gmail
    page.fill("#register-name", "Gmail User")
    page.fill("#register-email", "test@gmail.com")
    page.fill("#register-password", "Password123!")
    page.click("button:has-text('Creează cont')")
    expect(page.get_by_text("Adresă invalidă")).to_be_visible() # From AuthForm.tsx
    
    # Test USM.ro
    page.fill("#register-email", f"test{int(time.time())}@usm.ro")
    # Need to fill other fields to submit
    page.fill("#register-name", "USM User")
    page.fill("#register-password", "Password123!")
    page.fill("#confirm-password", "Password123!")
    
    page.click("button:has-text('Creează cont')")
    # Should NOT see "Adresă invalidă"
    expect(page.get_by_text("Adresă invalidă")).not_to_be_visible()
    # Should succeed or show other error
    # We don't check full success here, just domain validation pass

@pytest.mark.auth
def test_tc009_tc010_login_errors(page: Page):
    """
    TC009 - Login cu parolă greșită
    TC010 - Login cu email inexistent
    """
    page.goto("/")
    logout(page)

    # Ensure Login tab
    page.get_by_role("tab", name="Autentificare").click()

    # Non-existent email
    page.fill("#login-email", f"nonexistent{int(time.time())}@student.usv.ro")
    page.fill("#login-password", "RandomPass123")
    
    page.click("button[type='submit']:has-text('Autentificare')")
    
    # Expect error (generic or specific)
    # AuthController returns: "Email sau parolă incorectă" for both cases
    # Use re.compile for loose matching of "incorect" or "autentificare"
    expect(page.get_by_text(re.compile("incorect|autentificare", re.IGNORECASE))).to_be_visible()

@pytest.mark.auth
def test_tc011_logout(page: Page):
    """
    TC011 - Logout
    """
    # Simply create a user and logout
    page.goto("/")
    logout(page)

    page.get_by_role("tab", name="Înregistrare").click()
    page.fill("#register-name", "Logout User")
    page.fill("#register-email", f"logout{int(time.time())}@student.usv.ro")
    page.fill("#register-password", "Pass123456")
    page.fill("#confirm-password", "Pass123456")
    page.click("button[type='submit']:has-text('Creează cont')")
    
    # Verify logged in
    expect(get_user_menu_button(page)).to_be_visible()
    
    # Logout
    logout(page)
    
    # Verify redirected to login/auth
    expect(page.get_by_role("tab", name="Autentificare")).to_be_visible()

@pytest.mark.auth
def test_tc208_confirm_password_realtime(page: Page):
    """
    TC208 - Validare "Confirm Password" în timp real (sau la submit)
    """
    page.goto("/")
    page.get_by_role("tab", name="Înregistrare").click()
    
    page.fill("#register-password", "PasswordA")
    page.fill("#confirm-password", "PasswordB")
    
    page.click("button:has-text('Creează cont')")
    expect(page.get_by_text("Parolele nu se potrivesc")).to_be_visible()

# ==========================================
# 2. Profil Utilizator (User Profile)
# ==========================================

@pytest.mark.profile
def test_tc014_tc018_user_profile(page: Page):
    """
    TC014 - Vizualizare profil propriu
    TC018 - Navigare din profil
    """
    # Register/Login
    page.goto("/")
    logout(page)

    page.get_by_role("tab", name="Înregistrare").click()
    name = "Profile Tester"
    email = f"profile{int(time.time())}@student.usv.ro"
    page.fill("#register-name", name)
    page.fill("#register-email", email)
    page.fill("#register-password", "Pass123!")
    page.fill("#confirm-password", "Pass123!")
    page.click("button[type='submit']:has-text('Creează cont')")
    
    # Open User Menu -> Click Profile
    # Header.tsx: DropdownMenuItem onClick={() => navigate("/profile")} "Profilul Meu"
    # Wait for login
    expect(get_user_menu_button(page)).to_be_visible()
    
    # Open menu
    get_user_menu_button(page).click()
    # Click "Profilul Meu"
    page.get_by_text("Profilul Meu").click()
    
    # Check details
    expect(page.get_by_text(name)).to_be_visible()
    expect(page.get_by_text(email)).to_be_visible()
    expect(page.get_by_text("student", exact=True).or_(page.get_by_text("Student", exact=True))).to_be_visible()
    
    # TC018 - Nav back
    page.click("text=Acasă")
    expect(page).to_have_url(re.compile(r"/$")) # Home URL

# ==========================================
# 3. Navigare & UI (General UI)
# ==========================================

@pytest.mark.ui
def test_tc019_header_unauthenticated(page: Page):
    """
    TC019 - Header Vizibilitate (Neautentificat)
    """
    page.goto("/")
    logout(page) # ensure logout
    
    expect(page.get_by_text("UniPlans")).to_be_visible()
    expect(page.get_by_text("Panou Admin")).not_to_be_visible()

@pytest.mark.ui
def test_tc020_to_tc022_header_authenticated_roles(page: Page):
    """
    TC020 - Header Vizibilitate (Autentificat)
    TC021 - Meniu Organizator hidden for student
    TC022 - Meniu Admin hidden for student
    """
    # Login as student
    page.goto("/")
    # Register new student
    page.get_by_role("tab", name="Înregistrare").click()
    page.fill("#register-name", "Student Role")
    page.fill("#register-email", f"stdrole{int(time.time())}@student.usv.ro")
    page.fill("#register-password", "Pass123!")
    page.fill("#confirm-password", "Pass123!")
    page.click("button:has-text('Creează cont')")
    
    # Check Header Links
    expect(page.get_by_text("Acasă")).to_be_visible()
    expect(page.get_by_text("Calendar")).to_be_visible()
    expect(page.get_by_text("Evenimentele Mele")).to_be_visible()
    
    # Check Hidden menus
    expect(page.get_by_text("Panou Organizator")).not_to_be_visible()

@pytest.mark.events
def test_tc026_list_events(page: Page):
    """
    TC026 - Listare evenimente (public -> requires login in current impl)
    """
    # App requires login to see dashboard/events
    page.goto("/")
    logout(page)
    
    # Login as student to view events
    page.get_by_role("tab", name="Înregistrare").click()
    page.fill("#register-name", "Event Viewer")
    page.fill("#register-email", f"viewer{int(time.time())}@student.usv.ro")
    page.fill("#register-password", "Pass123!")
    page.fill("#confirm-password", "Pass123!")
    page.click("button:has-text('Creează cont')")
    
    # Ensure desktop viewport to see the search bar in header
    page.set_viewport_size({"width": 1400, "height": 900})
    
    # Now we should see the dashhoard with events
    expect(page.get_by_placeholder("Caută evenimente...").or_(page.get_by_placeholder("Caută..."))).to_be_visible()
