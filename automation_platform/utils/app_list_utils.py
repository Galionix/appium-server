# app_list_utils.py
"""
Утильные функции для работы со списком приложений (RecyclerView) на Android.
"""
from appium.webdriver.webdriver import WebDriver
from xml.etree import ElementTree
import time


def click_child_by_selectors_and_index(driver: WebDriver, parent_selector: dict, child_selector: dict, index: int = 0):
    """
    Находит ребёнка по селекторам и индексу, кликает по нему.
    parent_selector: dict, например {'resource-id': 'com.miui.home:id/apps_list_view', 'tag': 'androidx.recyclerview.widget.RecyclerView'}
    child_selector: dict, например {'tag': 'android.widget.RelativeLayout'}
    index: int, индекс ребёнка (по порядку среди подходящих)
    """
    xml = driver.page_source
    tree = ElementTree.fromstring(xml)
    parent = None
    for node in tree.iter():
        match = True
        if 'tag' in parent_selector and node.tag != parent_selector['tag']:
            continue
        for k, v in parent_selector.items():
            if k == 'tag':
                continue
            if node.attrib.get(k) != v:
                match = False
                break
        if match:
            parent = node
            break
    if parent is None:
        raise Exception('Родитель не найден')
    matched_children = []
    for child in parent:
        match = True
        if 'tag' in child_selector and child.tag != child_selector['tag']:
            continue
        for k, v in child_selector.items():
            if k == 'tag':
                continue
            if child.attrib.get(k) != v:
                match = False
                break
        if match:
            matched_children.append(child)
    if len(matched_children) <= index:
        raise Exception(f'Ребёнок с индексом {index} не найден')
    target_child = matched_children[index]
    bounds = target_child.attrib.get('bounds')
    if not bounds:
        raise Exception('Нет координат bounds у ребёнка')
    import re
    m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
    if not m:
        raise Exception('Неверный формат bounds')
    x1, y1, x2, y2 = map(int, m.groups())
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    driver.tap([(center_x, center_y)], 300)
    time.sleep(0.5)

# Пример использования:
# from automation_platform.utils.app_list_utils import click_first_app_in_list
# click_first_app_in_list(driver)
