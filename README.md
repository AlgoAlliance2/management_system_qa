# QA Automation Framework for Management System

This folder contains the automated testing framework for the Management System project, utilizing **Python**, **Pytest**, and **Playwright**.

## 📋 Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+**
- **Node.js** (required to run the target application)

## 🛠️ Installation and Setup

1. **Navigate to the QA folder:**
   ```bash
   cd management_system_qa
   ```

2. **Create a Python virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```
   *(You can also install `firefox` or `webkit` if needed)*

## 🚀 How to Run Tests

⚠️ **Important:** Ensure the target application (Backend and Frontend) is running locally before starting the tests.
- Backend: `http://localhost:3001`
- Frontend: `http://localhost:5173`

### Standard Run (Headless)
Run all tests in the background (without GUI):
```bash
pytest
```

### Visual Interface Run (Headed)
Watch the browser while it executes the tests (useful for debugging):
```bash
pytest --headed
```

### Slow Motion Run
Add a delay between actions to easier follow the steps (e.g., 500ms):
```bash
pytest --headed --slowmo 500
```

## 📁 Project Structure

```
management_system_qa/
├── tests/                 # Folder containing test files
│   └── test_smoke.py      # Basic tests (e.g., verify page load)
├── conftest.py            # Global Pytest configurations and fixtures
├── pytest.ini             # Default Pytest settings (base URL, flags)
├── requirements.txt       # List of Python dependencies
└── .gitignore             # Files excluded from version control
```

## ⚙️ Configuration

Main settings are located in `pytest.ini`. Here you can modify the base URL of the application:

```ini
[pytest]
base_url = http://localhost:5173
```

## 📚 Technologies Used

- **[Playwright](https://playwright.dev/python/)**: For browser automation.
- **[Pytest](https://docs.pytest.org/)**: The test runner framework.
- **[pytest-base-url](https://pypi.org/project/pytest-base-url/)**: Plugin for managing the base URL.