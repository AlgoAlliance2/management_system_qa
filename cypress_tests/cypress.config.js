const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    // Dacă vrei să testezi aplicația ta locală, lasă acest baseUrl
    // Dacă vrei să testezi alt site, poți comenta linia asta și folosi cy.visit('https://google.com')
    baseUrl: 'http://localhost:5173', 
    
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    // Dezactivează securitatea web pentru a permite vizitarea mai multor domenii în același test (opțional)
    chromeWebSecurity: false,
  },
});
