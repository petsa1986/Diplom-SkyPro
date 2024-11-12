from model.Kinopoisk_testing_api import Kinopoisk_testing_api
from model.Kinopoisk_testing_ui import Kinopoisk_testing_ui
import config
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


@pytest.fixture(scope="function")
def setup_auth_and_driver(test_config):
    """Объединенная фикстура для инициализации WebDriver и авторизации."""

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
            ), options=options)
    driver.get(test_config.base_url)
    driver.implicitly_wait(4)
    driver.maximize_window()

    # Имитация задержек перед действиями от пикчи
    sleep(2)

    # Инициализация объекта авторизации
    auth_ui = Kinopoisk_testing_ui(test_config)
    auth_ui.set_driver(driver)

    # Добавляем авторизационный токен в cookies
    token = test_config.auth_token
    domain = test_config.base_url.replace(
        "http://", "").replace(
            "https://", "").split("/")[0]
    driver.add_cookie({
        "name": "auth_token",
        "value": token,
        "path": "/",
        "domain": domain
    })
    driver.refresh()

    # Фикстура для клика на CAPTCHA checkbox
    try:
        # Ждем появления контейнера чекбокса
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'CheckboxCaptcha-Anchor')
                )
                )

        # Ожидаем, что кнопка станет кликабельной
        captcha_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'js-button'))
            )
        captcha_checkbox.click()

        # Проверка, что CAPTCHA пройдена (если возможно)
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(
                By.ID, 'js-button'
                ).get_attribute("aria-checked") == "true"
                )

    except Exception as e:
        print(f"Не удалось кликнуть на CAPTCHA checkbox: {e}")

    # Возвращаем как tuple, чтобы тесты могли использовать
    # как WebDriver, так и объект авторизации
    yield auth_ui, driver

    # Закрытие драйвера после теста
    driver.quit()


@pytest.fixture
def test_config():
    """Фикстура для доступа к переменным конфигурации из config.py"""
    return config


@pytest.fixture(scope="function")
def auth_api(test_config):
    """Fixture to set up the Authorization API client."""
    return Kinopoisk_testing_api(
        test_config.base_url_api, test_config.auth_token
        )