# Импорт тестового словаря и функций проверки экранов
from .screen_defs import TEST_SCREEN_DICT, is_feed_screen, is_dm_screen
# screens.py
"""
Структуры и функции для определения экранов Instagram и переходов между ними.
"""


# --- Переход: с главной в личные сообщения ---
from xml.etree import ElementTree
def go_to_dm(driver):
    """
    Кликает по кнопке входящих сообщений на главной.
    """
    xml = driver.page_source
    tree = ElementTree.fromstring(xml)
    for node in tree.iter():
        if node.attrib.get('resource-id') == 'com.instagram.android:id/action_bar_inbox_button':
            bounds = node.attrib.get('bounds')
            if bounds:
                import re
                m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if m:
                    x1, y1, x2, y2 = map(int, m.groups())
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    driver.tap([(center_x, center_y)], 300)
                    return True
    return False

# Пример использования:
# if is_feed_screen(driver.page_source):
#     go_to_dm(driver)
