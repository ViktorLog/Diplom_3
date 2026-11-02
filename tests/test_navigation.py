import allure

from pages.order_feed_page import OrderFeedPage
from pages.constructor_page import ConstructorPage
from routes import Routes


class TestNavigation:
    @allure.title('Ссылка ленты открывает список заказов')
    def test_feed_link_opens_order_feed(self, driver):
        page = ConstructorPage(driver)
        page.open()
        page.go_to_feed()

        page.wait_for_address(Routes.FEED_URL)
        assert OrderFeedPage(driver).heading_text() == "Лента заказов"

    @allure.title('Ссылка конструктора открывает сборку бургера')
    def test_constructor_link_opens_builder(self, driver):
        feed = OrderFeedPage(driver)
        feed.open()
        feed.go_to_constructor()

        feed.wait_for_address(Routes.BASE_URL)
        assert ConstructorPage(driver).heading_text() == "Соберите бургер"

