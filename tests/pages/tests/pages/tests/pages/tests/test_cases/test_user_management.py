import pytest
from playwright.sync_api import Page, expect
from tests.pages.login_page import LoginPage
from tests.pages.user_management_page import UserManagementPage
from conftest import TEST_USERNAME, TEST_PASSWORD, UPDATED_PASSWORD


class TestTC01NavigateToAdminModule:
    def test_navigate_to_admin_module(self, logged_in_page: Page):
        um = UserManagementPage(logged_in_page)
        um.navigate_to_admin()
        expect(logged_in_page).to_have_url(
            "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"
        )
        heading = logged_in_page.get_by_role("heading", name="System Users")
        expect(heading).to_be_visible()


class TestTC02AddNewUser:
    def test_add_new_user_successfully(self, user_mgmt: UserManagementPage):
        user_mgmt.click_add_user()
        user_mgmt.fill_user_role("ESS")
        user_mgmt.fill_employee_name("A")
        user_mgmt.fill_status("Enabled")
        user_mgmt.fill_username(TEST_USERNAME)
        user_mgmt.fill_password(TEST_PASSWORD)
        user_mgmt.click_save()
        expect(user_mgmt.page).to_have_url(
            "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers",
            timeout=10000,
        )


class TestTC03AddUserMissingFields:
    def test_add_user_missing_fields_shows_validation(self, user_mgmt: UserManagementPage):
        user_mgmt.click_add_user()
        user_mgmt.click_save()
        required_errors = user_mgmt.page.locator("text=Required")
        expect(required_errors.first).to_be_visible()


class TestTC04SearchNewUser:
    def test_search_newly_created_user(self, user_mgmt: UserManagementPage):
        user_mgmt.search_user(TEST_USERNAME)
        result_count = user_mgmt.get_search_result_count()
        assert result_count >= 1, f"Expected at least 1 result, got {result_count}"
        displayed_username = user_mgmt.get_first_result_username()
        assert TEST_USERNAME in displayed_username


class TestTC05SearchNonExistentUser:
    def test_search_nonexistent_user_returns_no_records(self, user_mgmt: UserManagementPage):
        user_mgmt.search_user("zzz_nonexistent_user_xyz")
        assert user_mgmt.is_no_records_found()


class TestTC06EditUserStatus:
    def test_edit_user_status(self, user_mgmt: UserManagementPage):
        user_mgmt.search_user(TEST_USERNAME)
        user_mgmt.page.wait_for_timeout(1000)
        user_mgmt.click_edit_on_first_result()
        user_mgmt.update_status("Disabled")
        user_mgmt.click_save()
        expect(user_mgmt.page).to_have_url(
            "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers",
            timeout=10000,
        )


class TestTC07EditUserPassword:
    def test_edit_user_password(self, user_mgmt: UserManagementPage):
        user_mgmt.search_user(TEST_USERNAME)
        user_mgmt.page.wait_for_timeout(1000)
        user_mgmt.click_edit_on_first_result()
        user_mgmt.update_password(UPDATED_PASSWORD)
        user_mgmt.click_save()
        expect(user_mgmt.page).to_have_url(
            "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers",
            timeout=10000,
        )


class TestTC08DeleteUser:
    def test_delete_user_and_verify_removed(self, user_mgmt: UserManagementPage):
        user_mgmt.delete_user_by_username(TEST_USERNAME)
        user_mgmt.page.wait_for_timeout(1500)
        user_mgmt.search_user(TEST_USERNAME)
        assert user_mgmt.is_no_records_found()
