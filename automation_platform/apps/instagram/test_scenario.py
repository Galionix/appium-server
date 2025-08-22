
# test_scenario.py
"""
Тестовый сценарий для Instagram: открытие приложения и проверка экрана.
"""
import time
from automation_platform.utils.device_utils import open_app, validate_screen
from automation_platform.apps.instagram.screen_defs import TEST_SCREEN_DICT

def test_scenario(driver):
    """
    Открывает Instagram, ждёт загрузки, проверяет, что открыт фид.
    Возвращает результат проверки.
    """
    open_app(driver, "instagram")
    time.sleep(5)  # Ждем открытия приложения
    validate_screen(TEST_SCREEN_DICT['feed']['check'], driver, 'feed')
    time.sleep(1)  # Дополнительная задержка для стабильности
    TEST_SCREEN_DICT['feed']['transitions']['to_dm'](driver)
    time.sleep(1)  # Ждем перехода в личные сообщения
    validate_screen(TEST_SCREEN_DICT['dm']['check'], driver, 'dm')
    time.sleep(1)  # Дополнительная задержка для стабильности
    return True
