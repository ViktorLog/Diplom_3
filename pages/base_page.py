import allure
from selenium.webdriver.common.action_chains import ActionChains
from locators.base_page import BasePageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def format_locator(self, locator, value):
        return (locator[0], locator[1].format(value))

    def dialog_is_closed(self):
        return not self.driver.find_elements(*BasePageLocators.MODAL)

    @allure.step("Открыть страницу {url}")
    def navigate_to(self, url):
        self.driver.get(url)

    def visible_element(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def enter_text(self, locator, text):
        self.visible_element(locator).send_keys(text)

    @allure.step("Нажать на элемент {locator}")
    def click(self, locator):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Закрыть всплывающее окно")
    def dismiss_dialog(self):
        def click_close(driver):
            button = EC.element_to_be_clickable(
                BasePageLocators.CLOSE_MODAL
            )(driver)

            if not button:
                return False

            try:
                button.click()
            except ElementClickInterceptedException:
                return False

            return True

        WebDriverWait(self.driver, 15).until(click_close)

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(BasePageLocators.MODAL)
        )
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(BasePageLocators.MODAL_OVERLAY)
        ) 

    def wait_for_address(self, url):
        WebDriverWait(self.driver, 15).until(EC.url_to_be(url))
        return self.driver.current_url

    @allure.step("Перейти в конструктор")
    def go_to_constructor(self):
        self.click(BasePageLocators.CONSTRUCTOR_LINK)

    @allure.step("Перейти в ленту заказов")
    def go_to_feed(self):
        self.click(BasePageLocators.FEED_LINK)

    def elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_until(self, condition, timeout=15):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Перенести компонент в область сборки")
    def transfer_component(self, ingredient, target):
        if self.driver.capabilities["browserName"] == "firefox":
            self.driver.execute_script("""
                const source = arguments[0];
                const target = arguments[1];
                const dataTransfer = new DataTransfer();

                function send(element, type) {
                    const rect = element.getBoundingClientRect();
                    element.dispatchEvent(new DragEvent(type, {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    }));
                }

                send(source, "dragstart");
                send(target, "dragenter");
                send(target, "dragover");
                send(target, "drop");
                send(source, "dragend");
            """, ingredient, target)
        else:
            ActionChains(self.driver).drag_and_drop(
                ingredient, target
            ).perform()
