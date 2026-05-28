# AccuKnox-user-management-tests

Automated test suite for the User Management module of OrangeHRM.
Built for the AccuKnox QA Trainee practical assessment.

## Tech Stack
- Python 3.10+
- Playwright 1.44.0
- pytest 8.2.0
- pytest-playwright 0.5.0

## Project Structure
- conftest.py
- pytest.ini
- requirements.txt
- tests/pages/login_page.py
- tests/pages/user_management_page.py
- tests/test_cases/test_user_management.py

## Setup

1. Install dependencies
pip install -r requirements.txt

2. Install Playwright browser
playwright install chromium

## How to Run Tests

Run all tests:
pytest

Run with details:
pytest -v

Run in browser (headed):
pytest --headed

## Test Cases Covered
- TC-01: Navigate to Admin Module
- TC-02: Add a New User
- TC-03: Add User with Missing Fields
- TC-04: Add User with Duplicate Username
- TC-05: Search for Created User
- TC-06: Search Non-Existent User
- TC-07: Edit User Status
- TC-08: Edit User Password
- TC-09: Edit User Mismatched Password
- TC-10: Delete User and Verify Removal

## Playwright Version
1.44.0
