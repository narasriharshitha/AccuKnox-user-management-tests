import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from tests.pages.login_page import LoginPage
from tests.pages.user_management_page import UserManagementPage

TEST_USERNAME = "qa_trainee_test01"
TEST_PASSWORD = "Admin@12345"
UPDATED_PASSWORD = "Admin@67890"

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    pg = context.new_page()
    yield pg
    pg.close()

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    login = LoginPage(page)
    login.navigate()
    login.login()
    return page

@pytest.fixture(scope="function")
def user_mgmt(logged_in_page: Page) -> UserManagementPage:
    um = UserManagementPage(logged_in_page)
    um.navigate_to_admin()
    return um
