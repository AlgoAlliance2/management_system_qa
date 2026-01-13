describe('TC-141: Flux Complet Creare și Participare Eveniment (End-to-End)', () => {
  const eventTitle = 'E2E Test Cypress Localhost';
  
  // Retrieve credentials from Cypress environment variables
  const orgUser = Cypress.env('orgUser');
  const adminUser = Cypress.env('adminUser');
  const studentUser = Cypress.env('studentUser');

  const getFutureDate = () => {
      const date = new Date();
      date.setDate(date.getDate() + 30);
      return date.toISOString().split('T')[0];
  };

  before(() => {
    // Basic connectivity check
    cy.request({
      url: 'http://localhost:8080/api/auth/register', // Check correct backend port
      failOnStatusCode: false
    }).then((resp) => {
      cy.log(`Backend Connectivity Check: Status ${resp.status}`);
    });
  });

  it('Execută pașii definiți în testul Python test_tc141_e2e_flow.py folosind localhost', () => {
    // Intercept login specifically for debugging
    cy.intercept('POST', '**/api/auth/login').as('loginRequest');

    // 1. Visit Localhost
    cy.visit('http://localhost:5176');
    
    // Ensure Logout if logged in
    cy.get('body').then(($body) => {
        if ($body.find('button svg.lucide-user').length > 0) {
            cy.get('button svg.lucide-user').closest('button').click();
            cy.contains('Deconectare').click();
        }
    });

    // 2. Organizer Login
    cy.log('Starting Organizer Login...');
    cy.get('#login-email').should('be.visible').clear().type(orgUser.email, { delay: 100 });
    cy.get('#login-password').clear().type(orgUser.password, { delay: 100 });
    cy.get('button[type="submit"]').contains('Autentificare').click();

    // Verify Login Request
    cy.wait('@loginRequest', { timeout: 10000 }).then((interception) => {
      if (interception.response.statusCode !== 200) {
        const bodyStr = JSON.stringify(interception.response.body);
        cy.log('LOGIN FAILED via API: ' + interception.response.statusCode);
        cy.log(bodyStr);
        throw new Error(`Login API Response was not 200 OK. Status: ${interception.response.statusCode}, Body: ${bodyStr}`);
      }
    });

    // Fail-fast check for error toast
    cy.get('body').then(($body) => {
      if ($body.text().includes('Eroare') || $body.text().includes('Incorect')) {
        throw new Error('Detected Error message on UI: ' + $body.text().substring(0, 100));
      }
    });

    // Verificăm UI-ul (folosim match parțial)
    cy.contains('Autentificare reu', { timeout: 15000 }).should('be.visible');
    cy.contains('UniPlans').should('be.visible');

    // 3. Create Event
    cy.contains('Cree', { timeout: 10000 }).should('be.visible'); // Creează
    cy.contains('Cree').first().click();
    
    // Dacă butonul nu ne-a dus la pagina corectă, mai facem un wait/check
    cy.location('pathname').should('include', 'create-event');

    // Form Step 1
    cy.get('#title').should('be.visible').type(eventTitle, { delay: 50 });
    cy.contains('button', 'Selectează categoria').click();
    cy.get('div[role="option"]').contains('Conferință').click();
    cy.get('#description').type('Descriere test Cypress pe localhost.', { delay: 20 });
    cy.contains('button', 'Continuă').click();

    // Form Step 2
    cy.contains('Dată, oră', { timeout: 5000 }).should('be.visible');
    const futureDate = getFutureDate();
    cy.get('#date').type(futureDate);
    cy.get('#startTime').type('10:00');
    cy.get('#endTime').type('12:00');
    cy.get('#location').type('Corp A, Sala C1', { delay: 50 });
    cy.contains('button', 'Continuă').click();

    // Form Step 3
    cy.contains('Imagine și revizuire').should('be.visible');
    cy.contains('button', 'Creează eveniment').should('be.visible');
    cy.wait(500); 
    cy.contains('button', 'Creează eveniment').click();
    
    cy.get('body').contains('Eveniment creat cu succes').should('be.visible'); 
    cy.wait(2000); 

    // Logout Organizer
    cy.get('button svg.lucide-user').closest('button').click();
    cy.contains('Deconectare').click();

    // 4. Admin Login
    cy.get('#login-email').should('be.visible').clear().type(adminUser.email, { delay: 100 });
    cy.get('#login-password').should('be.visible').clear().type(adminUser.password, { delay: 100 });
    cy.get('button[type="submit"]').contains('Autentificare').click();
    
    cy.contains('Autentificare reu', { timeout: 10000 }).should('be.visible');
    cy.wait(2000);
    
    // Visit Admin Panel
    cy.visit('http://localhost:5173/admin');

    // Approve Event
    cy.contains('Aprobării', { timeout: 10000 }).should('be.visible'); // În Așteptarea Aprobării
    
    // Find the specific card
    cy.contains('div.bg-white', eventTitle)
      .should('be.visible')
      .within(() => {
          cy.contains('button', 'Revizuiește Evenimentul').click();
      });

    cy.contains('Revizuire Necesară').should('be.visible');
    cy.contains('button', 'Aprobă Evenimentul').click();
    cy.contains('Eveniment aprobat cu succes!').should('be.visible');

    // Logout Admin
    cy.get('button svg.lucide-user').closest('button').click();
    cy.contains('Deconectare').click();
  });
});
