# device_utils.py
"""
Утильные функции для работы с Android-устройством через Appium.
"""
from appium.webdriver.webdriver import WebDriver
from automation_platform.utils.app_list_utils import click_child_by_selectors_and_index
import time


def open_app(driver: WebDriver, appname: str):
    """
    Открывает список приложений на устройстве:
    1. Нажимает кнопку Home
    2. Делает свайп снизу вверх
    3. Нажимает на плашку поиска (координаты нужно уточнить)
    """
    # 1. Нажать Home (альтернативные способы)
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

    # 2. Свайп снизу вверх для открытия списка приложений
    driver.swipe(start_x=500, start_y=2000, end_x=500, end_y=500, duration=500)
    time.sleep(0.5)

    # 3. Нажать на плашку поиска
    driver.tap([(447, 2234)], 500)
    time.sleep(0.5)


    # 4. Ввести текст 'instagram' в активное поле
    driver.execute_script("mobile: type", {"text": appname})
    time.sleep(0.5)

    # 5. Открыть первое приложение в списке
    click_child_by_selectors_and_index(
        driver,
        {'resource-id': 'com.miui.home:id/apps_list_view', 'tag': 'androidx.recyclerview.widget.RecyclerView'},
        {'tag': 'android.widget.RelativeLayout'},
        index=1  # Индекс 1, т.к. 0 - это открыть в гугл плей
    )

    # 3. Нажать на плашку поиска (примерные координаты)
    # TODO: подобрать координаты под конкретное устройство
    # search_x = 447
    # search_y = 2234
    # action = TouchAction(driver)
    # action.tap(x=search_x, y=search_y).perform()
    # time.sleep(0.3)

    # Дальнейшие шаги: ввод текста, выбор приложения
    # ...

# Пример использования:
# from automation_platform.utils.device_utils import open_app_drawer
# open_app_drawer(driver)
def validate_screen(check_func, driver, screen_name):
    """
    Валидирует, что мы на нужном экране. Если нет — кидает ошибку.
    """
    if not check_func(driver.page_source):
        raise RuntimeError(f"Screen validation failed: not on '{screen_name}' (check function {check_func.__name__})")