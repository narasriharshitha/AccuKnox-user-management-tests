from playwright.sync_api import Page, expect


class UserManagementPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_admin(self):
        self.page.get_by_role("link", name="Admin").click()
        self.page.wait_for_url("**/admin/viewSystemUsers", timeout=10000)
        self.page.wait_for_load_state("networkidle")

    def click_add_user(self):
        self.page.get_by_role("button", name="Add").click()
        self.page.wait_for_url("**/admin/saveSystemUser", timeout=10000)
        self.page.wait_for_load_state("networkidle")

    def fill_user_role(self, role: str = "ESS"):
        dropdown = self.page.locator(".oxd-select-text").nth(0)
        dropdown.click()
        self.page.get_by_role("option", name=role).click()

    def fill_employee_name(self, name: str):
        emp_input = self.page.get_by_placeholder("Type for hints...")
        emp_input.fill(name)
        self.page.wait_for_selector(".oxd-autocomplete-option", timeout=8000)
        self.page.locator(".oxd-autocomplete-option").first.click()

    def fill_status(self, status: str = "Enabled"):
        dropdown = self.page.locator(".oxd-select-text").nth(1)
        dropdown.click()
        self.page.get_by_role("option", name=status).click()

    def fill_username(self, username: str):
        self.page.locator("input[autocomplete='off']").nth(0).fill(username)

    def fill_password(self, password: str):
        password_fields = self.page.locator("input[type='password']")
        password_fields.nth(0).fill(password)
        password_fields.nth(1).fill(password)

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

    def search_user(self, username: str):
        self.page.wait_for_selector("input[placeholder='Username']", timeout=8000)
        self.page.locator("input[placeholder='Username']").fill(username)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle")

    def get_search_result_count(self) -> int:
        rows = self.page.locator(".oxd-table-body .oxd-table-row")
        return rows.count()

    def get_first_result_username(self) -> str:
        return self.page.locator(
            ".oxd-table-body .oxd-table-row .oxd-table-cell:nth-child(3)"
        ).first.inner_text()

    def click_edit_on_first_result(self):
        edit_btn = self.page.locator(
            ".oxd-table-body .oxd-table-row"
        ).first.get_by_role("button").nth(1)
        edit_btn.click()
        self.page.wait_for_load_state("networkidle")

    def update_status(self, status: str):
        dropdown = self.page.locator(".oxd-select-text").nth(1)
        dropdown.click()
        self.page.get_by_role("option", name=status).click()

    def update_password(self, new_password: str):
        self.page.locator("label", has_text="Change Password").click()
        self.page.wait_for_timeout(500)
        password_fields = self.page.locator("input[type='password']")
        password_fields.nth(0).fill(new_password)
        password_fields.nth(1).fill(new_password)

    def get_current_username_value(self) -> str:
        return self.page.locator("input[autocomplete='off']").nth(0).input_value()

    def delete_first_result(self):
        delete_btn = self.page.locator(
            ".oxd-table-body .oxd-table-row"
        ).first.get_by_role("button").nth(0)
        delete_btn.click()
        self.page.get_by_role("button", name="Yes, Delete").click()
        self.page.wait_for_load_state("networkidle")

    def delete_user_by_username(self, username: str):
        self.search_user(username)
        self.page.wait_for_timeout(1000)
        if self.get_search_result_count() > 0:
            self.delete_first_result()

    def get_toast_message(self) -> str:
        toast = self.page.locator(".oxd-toast-content")
        toast.wait_for(state="visible", timeout=8000)
        return toast.inner_text()

    def is_no_records_found(self) -> bool:
        return self.page.locator("text=No Records Found").is_visible()
