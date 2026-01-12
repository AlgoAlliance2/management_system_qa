# QA Automation Framework for Management System

This folder contains the automated testing framework for the Management System project. It includes two distinct testing suites:
1. **Python/Playwright** for functional and integration testing.
2. **Cypress** for End-to-End (E2E) UI testing.

## Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+**
- **Node.js** (v14+)

## Python / Playwright Tests

### Installation

1. **Navigate to the QA folder:**
   ```bash
   cd management_system_qa
   ```

2. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate # Linux/Mac
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

### Running Python Tests

Run all tests interactively:
```bash
pytest
```

**Run with Reporting (Recommended):**
To generate timestamped HTML reports in `test_reports/`:
```bash
python run_tests_with_report.py
```
You can also pass arguments locally:
```bash
python run_tests_with_report.py tests/test_requirements_coverage.py
```

Run specific test file:
```bash
pytest tests/test_requirements_coverage.py
```

## Cypress Tests

The Cypress E2E tests are located in the `cypress_tests` directory.

### Installation

1. **Navigate to the Cypress folder:**
   ```bash
   cd management_system_qa/cypress_tests
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

### Running Cypress Tests

Open Interactive GUI:
```bash
npm run cypress:open
```

Run Headless (CI/CD):
```bash
npm run cypress:run
```

## Configuration

### Python
- Configured via `pytest.ini`.
- Base URL: `http://localhost:5173`

### Cypress
- Configured via `cypress_tests/cypress.config.js`.
- Base URL: `http://localhost:5173`


6. **Environment Configuration:**
   The framework requires connection to the MongoDB database to seed test users and valid credentials to run tests.
   - Ensure the `MONGO_URI` environment variable is set.
   - Setup the following environment variables for test accounts (defaults are provided but overriding is recommended for security):
     - `TEST_ADMIN_PASSWORD`
     - `TEST_STUDENT_PASSWORD`
     - `TEST_ORG_PASSWORD`
     - `TEST_USER_PASSWORD`
   - By default, the scripts attempt to load these from `../management_system_back/app/.env`.

7. **Seed Test Data:**
   Before running tests, ensure the database has the required test users (Admin, Organizer, Student):
   ```bash
   python ensure_test_users.py
   ```
   *Note: This script requires `MONGO_URI` to be available.*

## How to Run Tests

⚠️ **Important:** Ensure the target application (Backend and Frontend) is running locally before starting the tests.
- Backend: `http://localhost:3001`
- Frontend: `http://localhost:5173`

### Troubleshooting: "pytest command not found"
If running `pytest` gives an error, make sure your virtual environment is active. Alternatively, use the direct path to the Python executable in your venv:
`.\venv\Scripts\python -m pytest`

### 1. Run All Tests
```bash
pytest
```

### 2. Run Specific Categories (Markers)
We have newly added test categories. Use the `-m` flag:

- **Security Tests** (XSS, Injection, Auth):
  ```bash
  pytest -m security
  ```
- **Functional Tests** (User flows, Events):
  ```bash
  pytest -m functional
  ```
- **Usability Tests** (UI/UX, Responsiveness):
  ```bash
  pytest -m usability
  ```
- **Penetration Tests** (Brute force, Fuzzing):
  ```bash
  pytest -m penetration
  ```
- **Smoke Tests** (Basic health checks):
  ```bash
  pytest -m smoke
  ```

### 3. Run Specific Test Files
```bash
pytest tests/test_functional.py
```

### Visual Interface Run (Headed)
Watch the browser actions:
```bash
pytest --headed --slowmo 500
```

## Project Structure

```
management_system_qa/
├── tests/                 # Folder containing test files
│   └── test_smoke.py      # Basic tests (e.g., verify page load)
├── conftest.py            # Global Pytest configurations and fixtures
├── ensure_test_users.py   # Script to seed database with test users
├── pytest.ini             # Default Pytest settings (base URL, flags)
├── requirements.txt       # List of Python dependencies
└── .gitignore             # Files excluded from version control
```

## Configuration

Main settings are located in `pytest.ini`. Here you can modify the base URL of the application:

```ini
[pytest]
base_url = http://localhost:5173
```

## Technologies Used

- **[Playwright](https://playwright.dev/python/)**: For browser automation.
- **[Pytest](https://docs.pytest.org/)**: The test runner framework.
- **[pytest-base-url](https://pypi.org/project/pytest-base-url/)**: Plugin for managing the base URL.
- **[PyMongo](https://pymongo.readthedocs.io/)**: For database interactions (seeding data).
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: For managing environment variables.