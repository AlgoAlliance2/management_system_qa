describe('Internal & External Connectivity Test', () => {
    it('Should load Google Homepage', () => {
      // Direct visit is allowed for single superdomain per test without cy.origin if Config allows it
      // But simpler check:
      cy.request('https://www.google.com').should((response) => {
        expect(response.status).to.eq(200);
      });
    });
  });

describe('Management System - Core Functionality', () => {
  const timestamp = Date.now();
  const user = {
      name: 'Test User',
      email: `test${timestamp}@student.usv.ro`,
      password: 'Password123!'
  };

  it('Should register, login, and see the main application', () => {
      // INTERCEPT AND FIX LOCALHOST CALLS
      cy.intercept('*', (req) => {
        if (req.url.includes('localhost:8080')) {
            req.url = req.url.replace('localhost:8080', '127.0.0.1:8080');
        }
      });
      
      // 1. Visit the local app
      cy.visit('/');

      // 2. Register
      cy.contains('button', 'Înregistrare').click();
      
      cy.get('#register-name').type('Testing User');
      // Dynamic email to ensure unique registration
      cy.get('#register-email').type(user.email);
      cy.get('#register-password').type(user.password);
      cy.get('#confirm-password').type(user.password);
      
      cy.contains('button', 'Creează cont').click();

      // 3. Verify Landing on Main Page (Authenticated)
      // Wait for network response first? No, UI check is better.
      // If header is missing, maybe registration failed?
      // Check for error toast.
      cy.get('body').then(($body) => {
          if ($body.find('.text-red-500').length > 0) {
              const err = $body.find('.text-red-500').text();
              cy.log('REGISTRATION ERROR: ' + err);
          }
      });
      
      // We know port 8080 is backend.
      // Frontend is at baseUrl (5173).
      // Check if header appears.
      cy.get('header', { timeout: 15000 }).should('exist');
      
      // 4. Verify User Menu exists (Lucide Icon)
      cy.get('svg.lucide-user').should('exist');

      // 5. Simple Navigation Check (Go to Calendar)
      cy.contains('a', 'Calendar').click();
      cy.url().should('include', '/calendar');
  });
});
