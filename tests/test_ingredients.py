import allure

from ingredients import IngredientSamples
from pages.constructor_page import ConstructorPage


class TestIngredients:
    @allure.title('Карточка показывает детали выбранного ингредиента')
    def test_card_opens_correct_ingredient(self, driver):
        page = ConstructorPage(driver)
        page.open()

        assert page.show_ingredient_details(IngredientSamples.BUN) == "Детали ингредиента"
        assert page.details_name() == IngredientSamples.BUN

    @allure.title('Закрытие окна с деталями ингредиента')
    def test_close_button_hides_details(self, driver):
        page = ConstructorPage(driver)
        page.open()
        page.show_ingredient_details(IngredientSamples.BUN)

        page.dismiss_dialog()

        assert page.dialog_is_closed()

    @allure.title('Добавленная булка увеличивает количество на карточке')
    def test_adding_bun_increases_quantity(self, driver):
        page = ConstructorPage(driver)
        page.open()
        before = page.ingredient_quantity(IngredientSamples.BUN)

        page.put_ingredient_in_burger(IngredientSamples.BUN)

        assert page.wait_for_quantity(IngredientSamples.BUN, before + 2)

