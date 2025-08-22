# dm_feed.py
"""
Переход из личных сообщений в фид Instagram.
"""
from xml.etree import ElementTree
import re

def dm_feed(driver):
    """
    Кликает по элементу <android.widget.ImageView ... resource-id="com.instagram.android:id/action_bar_navigation_button"> на экране личных сообщений.
    """
    xml = driver.page_source
    tree = ElementTree.fromstring(xml)
    for node in tree.iter('android.widget.ImageView'):
        if node.attrib.get('resource-id') == 'com.instagram.android:id/action_bar_navigation_button':
            bounds = node.attrib.get('bounds')
            if bounds:
                m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if m:
                    x1, y1, x2, y2 = map(int, m.groups())
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    driver.tap([(center_x, center_y)], 300)
                    return True
    return False
