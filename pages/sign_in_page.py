import allure
from locators.sign_in_locators import SignInPageLocators

from pages.base_page import BasePage
from routes import Routes


class SignInPage(BasePage):

    def open(self):
        self.navigate_to(Routes.LOGIN_URL)

    @allure.step("Войти в аккаунт тестового пользователя")
    def login(self, email, password):
        self.enter_text(SignInPageLocators.EMAIL, email)
        self.enter_text(SignInPageLocators.PASSWORD, password)
        self.click(SignInPageLocators.LOGIN_BUTTON)
        self.wait_for_address(Routes.BASE_URL)
