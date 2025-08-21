from time import sleep
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

# Импортируем наши функции
from instagram_utils import check_instagram_feed_opened, open_instagram_from_home, check_messages_screen_opened, click_on_new_messages

# Capabilities для подключения к текущему состоянию телефона
capabilities = {
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:deviceName": "MyPhone",
    "appium:noReset": True,
    "appium:fullReset": False,
    
    # Увеличиваем таймауты
    "appium:androidInstallTimeout": 180000,
    "appium:adbExecTimeout": 120000,
    "appium:uiautomator2ServerInstallTimeout": 120000,
}

options = UiAutomator2Options().load_capabilities(capabilities)
options.udid = "6d834b8d0421"

remote = webdriver.__dict__.get("Remote")
driver = remote("http://127.0.0.1:4723", options=options) # pyright: ignore[reportOptionalCall]

sleep(2)

driver.press_keycode(26)  # KEYCODE_POWER
sleep(1)

# Свайп для разблокировки
driver.swipe(start_x=500, start_y=1500, end_x=500, end_y=500, duration=500)
sleep(1)

# # Используем функцию из модуля
# if open_instagram_from_home(driver):
#     sleep(2)
#     print("✅ Тест пройден: Instagram открыт на главной странице!")
    
#     # Проверяем что мы на главной странице
#     if check_instagram_feed_opened(driver):
#         sleep(2)
        
#         # Кликаем по кнопке сообщений
#         try:
#             inbox_button = driver.find_element("id", "com.instagram.android:id/action_bar_inbox_button")
#             inbox_button.click()
#             sleep(3)  # Ждем загрузки экрана сообщений
#             print("✅ Кнопка сообщений нажата!")
            
#             # Проверяем, что открылся экран сообщений
#             if check_messages_screen_opened(driver):
#                 print("✅ Экран сообщений открыт!")
                
#                 # Ищем и кликаем по чатам с новыми сообщениями
#                 if click_on_new_messages(driver):
#                     print("🎉 Успешно открыт чат с новыми сообщениями!")
#                 else:
#                     print("ℹ️ Новых сообщений не найдено")
                    
#             else:
#                 print("❌ Не удалось открыть экран сообщений")
                
#         except Exception as e:
#             print(f"❌ Ошибка при работе с кнопкой сообщений: {e}")
            
# else:
#     print("❌ Тест не пройден: не удалось открыть Instagram")

sleep(3)
driver.quit()