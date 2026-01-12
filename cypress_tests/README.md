# Management System E2E Testing (Cypress)

Acest folder conține suita de teste automate E2E (End-to-End) pentru aplicația "Management System", realizată folosind framework-ul **Cypress**.

Acest proiect este configurat să ruleze independent de codul sursă al aplicației (frontend/backend), permițând testarea oricărui mediu (local sau remote).

## 📋 Cerințe preliminare

*   [Node.js](https://nodejs.org/) instalat (versiunea 14+ recomandată).

## 🚀 Instalare

1.  Deschideți un terminal în acest folder:
    ```bash
    cd management_system_cypress
    ```
2.  Instalați dependențele:
    ```bash
    npm install
    ```

## 🏃‍♂️ Rulare Teste

### Interfața Vizuală (GUI)
Pentru a deschide interfața Cypress și a vedea testele rulând în timp real:

```bash
npm run cypress:open
```
*Se va deschide o fereastră. Alegeți "E2E Testing" și apoi browserul dorit (ex: Chrome).*

### Rulare în linie de comandă (Headless)
Pentru a rula toate testele în fundal (fără interfață grafică), utile pentru CI/CD:

```bash
npm run cypress:run
```

## 📂 Structura Proiectului

*   `cypress/e2e/` - Aici se află fișierele cu teste (ex: `sample_test.cy.js`).
*   `cypress.config.js` - Fișierul de configurare Cypress (Base URL, setări browser, etc.).

## ⚙️ Configurare

Dacă doriți să schimbați adresa aplicației testate (implicit `http://localhost:5173`), editați fișierul `cypress.config.js`:

```javascript
module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173', // Modificați aici URL-ul
    // ...
  },
});
```
