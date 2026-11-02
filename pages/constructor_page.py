import allure
from locators.constructor_locators import ConstructorPageLocators

from ingredients import IngredientSamples
from pages.base_page import BasePage
from routes import Routes


class ConstructorPage(BasePage):

    def open(self):
        self.navigate_to(Routes.BASE_URL)
        self.visible_element(ConstructorPageLocators.TITLE)

    def ingredient_card(self, name):
        return self.format_locator(ConstructorPageLocators.INGREDIENT, name)

    def ingredient_badge(self, name):
        return self.format_locator(ConstructorPageLocators.INGREDIENT_COUNTER, name)

    def heading_text(self):
        return self.visible_element(ConstructorPageLocators.TITLE).text

    @allure.step("Открыть детали ингредиента {name}")
    def show_ingredient_details(self, name):
        self.click(self.ingredient_card(name))
        return self.visible_element(ConstructorPageLocators.DETAILS_TITLE).text

    def open_bun_details(self):
        return self.show_ingredient_details(IngredientSamples.BUN)

    def bun_quantity(self):
        return self.ingredient_quantity(IngredientSamples.BUN)

    def add_bun(self):
        self.put_ingredient_in_burger(IngredientSamples.BUN)

    def wait_for_bun_quantity(self, expected):
        return self.wait_for_quantity(IngredientSamples.BUN, expected)

    def details_name(self):
        return self.visible_element(ConstructorPageLocators.DETAILS_NAME).text

    def ingredient_quantity(self, name):
        return int(self.visible_element(self.ingredient_badge(name)).text)

    @allure.step("Добавить ингредиент {name} в заказ")
    def put_ingredient_in_burger(self, name):
        ingredient = self.visible_element(self.ingredient_card(name))
        target = self.visible_element(ConstructorPageLocators.DROP_AREA)

        self.transfer_component(ingredient, target)

    def wait_for_quantity(self, name, expected):
        def counter_matches(driver):
            return self.ingredient_quantity(name) == expected

        return self.wait_until(counter_matches)

    @allure.step("Собрать бургер и оформить заказ")
    def place_order(self):
        self.put_ingredient_in_burger(IngredientSamples.BUN)
        self.wait_for_quantity(IngredientSamples.BUN, 2)
        self.put_ingredient_in_burger(IngredientSamples.FILLING)
        self.wait_for_quantity(IngredientSamples.FILLING, 1)
        self.click(ConstructorPageLocators.ORDER_BUTTON)
        return self.wait_until(self.read_created_order_number, timeout=45)

    def read_created_order_number(self, driver):
        elements = self.elements(ConstructorPageLocators.ORDER_NUMBER)
        if elements and elements[0].is_displayed():
            text = elements[0].text
            if text.isdigit() and int(text) > 0 and text != "9999":
                return int(text)
        return False
