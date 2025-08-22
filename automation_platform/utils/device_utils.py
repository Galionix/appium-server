def is_package_opened(driver: 'WebDriver', package_name: str) -> bool:
    """
    Проверяет, открыт ли сейчас нужный package на устройстве.
    """
    try:
        # Получаем XML текущего экрана
        xml = driver.page_source
        return f'package="{package_name}"' in xml or f'package=\"{package_name}\"' in xml
    except Exception:
        return False
# device_utils.py
"""
Утильные функции для работы с Android-устройством через Appium.
"""
from appium.webdriver.webdriver import WebDriver
from automation_platform.utils.app_list_utils import click_child_by_selectors_and_index
import time


def open_app(driver: WebDriver, appname: str):
    """
    Открывает приложение, если оно ещё не запущено.
    """
    # Если нужный package уже открыт — ничего не делаем
    package_map = {
        'instagram': 'com.instagram.android',
        # можно добавить другие приложения
    }
    package_name = package_map.get(appname.lower(), appname)
    if is_package_opened(driver, package_name):
        return

    # ...existing code...
    driver.press_keycode(3)  # KEYCODE_HOME
    time.sleep(0.5)
    driver.keyevent(3)
    time.sleep(0.5)
    driver.press_keycode(3)  # KEYCODE_HOME
    time.sleep(0.5)
    driver.keyevent(3)
    time.sleep(0.5)
    driver.press_keycode(3)  # KEYCODE_HOME
    time.sleep(0.5)
    driver.keyevent(3)
    time.sleep(0.5)
    driver.swipe(start_x=500, start_y=2000, end_x=500, end_y=500, duration=500)
    time.sleep(0.5)
    driver.tap([(447, 2234)], 500)
    time.sleep(0.5)
    driver.execute_script("mobile: type", {"text": appname})
    time.sleep(0.5)
    click_child_by_selectors_and_index(
        driver,
        {'resource-id': 'com.miui.home:id/apps_list_view', 'tag': 'androidx.recyclerview.widget.RecyclerView'},
        {'tag': 'android.widget.RelativeLayout'},
        index=1
    )

# Пример использования:
# from automation_platform.utils.device_utils import open_app_drawer
# open_app_drawer(driver)
def validate_screen(check_func, driver, screen_name):
    """
    Валидирует, что мы на нужном экране. Если нет — кидает ошибку.
    """
    if not check_func(driver.page_source):
        raise RuntimeError(f"Screen validation failed: not on '{screen_name}' (check function {check_func.__name__})")