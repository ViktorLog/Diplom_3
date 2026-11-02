import allure
from locators.order_feed_locators import OrderFeedPageLocators

from pages.base_page import BasePage
from routes import Routes


class OrderFeedPage(BasePage):

    def open(self):
        self.navigate_to(Routes.FEED_URL)
        self.visible_element(OrderFeedPageLocators.TITLE)

    def heading_text(self):
        return self.visible_element(OrderFeedPageLocators.TITLE).text

    @allure.step("Получить счетчик {period}")
    def completed_orders(self, period):
        locator = OrderFeedPageLocators.TOTAL if period == "total" else OrderFeedPageLocators.TODAY
        return int(self.visible_element(locator).text)

    @allure.step("Дождаться увеличения счетчика {period}")
    def wait_for_completed_orders_growth(self, period, previous):
        def count_increased(driver):
            current = self.completed_orders(period)
            if current > previous:
                return current
            return False

        return self.wait_until(count_increased, timeout=30)

    @allure.step("Дождаться заказа {number} в разделе В работе")
    def wait_for_preparing_order(self, number):
        def contains_order(driver):
            for item in self.elements(OrderFeedPageLocators.IN_PROGRESS):
                if item.text.isdigit() and int(item.text) == number:
                    return True
            return False
        return self.wait_until(contains_order, timeout=30)
