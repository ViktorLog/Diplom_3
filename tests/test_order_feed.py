import allure
import pytest

from pages.order_feed_page import OrderFeedPage
from pages.constructor_page import ConstructorPage


class TestOrderFeed:
    @allure.title('Счетчик выполненных заказов растет после оформления')
    @pytest.mark.parametrize("period", ["total", "today"])
    def test_new_order_increases_completed_count(self, signed_in_driver, period):
        feed = OrderFeedPage(signed_in_driver)
        feed.open()
        before = feed.completed_orders(period)
        feed.go_to_constructor()
        main = ConstructorPage(signed_in_driver)

        main.place_order()
        main.dismiss_dialog()
        main.go_to_feed()

        after = feed.wait_for_completed_orders_growth(period, before)
        assert after > before

    @allure.title("Номер оформленного заказа появляется в разделе В работе")
    def test_new_order_appears_in_preparing_list(self, signed_in_driver):
        main = ConstructorPage(signed_in_driver)

        number = main.place_order()
        main.dismiss_dialog()
        main.go_to_feed()

        assert OrderFeedPage(signed_in_driver).wait_for_preparing_order(number)
