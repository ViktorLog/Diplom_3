import pytest
from selenium import webdriver

from pages.sign_in_page import SignInPage
from helpers import make_account_data, create_account, remove_account


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(options=options)
    browser.set_window_size(1440, 1000)
    yield browser
    browser.quit()


@pytest.fixture
def test_account():
    account_payload = make_account_data()
    token = create_account(account_payload)
    yield account_payload
    remove_account(token)


@pytest.fixture
def signed_in_driver(driver, test_account):
    page = SignInPage(driver)
    page.open()
    page.login(test_account["email"], test_account["password"])
    return driver
