# screen_defs.py
"""
Тестовые структуры и функции для распознавания экранов Instagram.
"""
from xml.etree import ElementTree

from automation_platform.apps.instagram.navigation.dm_feed import dm_feed
from automation_platform.apps.instagram.navigation.feed_dm import feed_dm

# --- Экран: Главная (фид) ---
def is_feed_screen(xml: str) -> bool:
    tree = ElementTree.fromstring(xml)
    for node in tree.iter():
        if node.attrib.get('resource-id') == 'com.instagram.android:id/tab_bar':
            for child in node:
                if child.attrib.get('resource-id') == 'com.instagram.android:id/feed_tab' and \
                   child.attrib.get('content-desc', '').lower() in ['дом', 'home']:
                    return True
    return False

# --- Экран: Личные сообщения ---
def is_dm_screen(xml: str) -> bool:
    tree = ElementTree.fromstring(xml)
    for node in tree.iter():
        if node.attrib.get('resource-id') == 'com.instagram.android:id/inbox_refreshable_thread_list_recyclerview':
            return True
    return False

# --- Тестовый словарь для примера ---
TEST_SCREEN_DICT = {
    'feed': {
        'resource-id': 'com.instagram.android:id/tab_bar',
        'desc': 'Главная страница (фид)',
        'check': is_feed_screen,
        'transitions': {
            'to_dm': feed_dm,
            'to_profile': 'profile',
            # Добавьте другие переходы по необходимости
        }
    },
    'dm': {
        'resource-id': 'com.instagram.android:id/direct_thread_list_recycler_view',
        'desc': 'Личные сообщения',
        'check': is_dm_screen,
        'transitions': {
            'to_feed': dm_feed,
            # Добавьте другие переходы по необходимости
        }
    },
    'dm_button': {
        'resource-id': 'com.instagram.android:id/action_bar_inbox_button',
        'desc': 'Кнопка входящих сообщений',
        'check': None,
        'transitions': {}
    }
}