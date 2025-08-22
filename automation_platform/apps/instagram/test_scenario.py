# Универсальная функция валидации и перехода к нужному экрану
from automation_platform.apps.instagram.metrics.dm_get_new_requests import count_new_dm_requests
from automation_platform.apps.instagram.screen_defs import TEST_SCREEN_DICT
from automation_platform.utils.need_screen import need_screen


# test_scenario.py
"""
Тестовый сценарий для Instagram: открытие приложения и проверка экрана.
"""
import time
from automation_platform.utils.device_utils import open_app
# from automation_platform.apps.instagram.screen_defs import TEST_SCREEN_DICT

def test_scenario(driver):
    """
    Открывает Instagram, ждёт загрузки, проверяет, что открыт фид.
    Возвращает результат проверки.
    """
    open_app(driver, "instagram")
    time.sleep(1)  # Ждем открытия приложения
    need_screen(driver, TEST_SCREEN_DICT, 'feed')
    # time.sleep(1)  # Дополнительная задержка для стабильности
    # TEST_SCREEN_DICT['feed']['transitions']['to_dm'](driver)
    time.sleep(1)  # Ждем перехода в личные сообщения
    # need_screen(driver, TEST_SCREEN_DICT, 'dm')
    # newRequests = count_new_dm_requests(driver.page_source)
    # if newRequests > 0:
    #     print(f"Новые запросы в директ: {newRequests}")
    # else:
    #     print("Нет новых запросов в директ.")
    # time.sleep(1)  # Дополнительная задержка для стабильности
    return True
