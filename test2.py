from time import sleep
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

# Capabilities для подключения к текущему состоянию телефона (без запуска приложения)
capabilities = {
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:deviceName": "MyPhone",
    # Убираем appPackage и appActivity - просто подключаемся к текущему состоянию
    "appium:noReset": True,
    "appium:fullReset": False,
    
    # Увеличиваем таймауты
    "appium:androidInstallTimeout": 180000,
    "appium:adbExecTimeout": 120000,
    "appium:uiautomator2ServerInstallTimeout": 120000,
}

options = UiAutomator2Options().load_capabilities(capabilities)
options.udid = "6d834b8d0421"

remote = webdriver.__dict__.get("Remote")  # Получаем Remote из appium.webdriver
# Подключение к телефону
driver = remote("http://127.0.0.1:4723", options=options) # pyright: ignore[reportOptionalCall]

sleep(2)

# Нажимаем кнопку Home
driver.press_keycode(3)  # 3 = KEYCODE_HOME
print("Нажали кнопку Home")

sleep(2)
driver.save_screenshot("home_screen.png")
# instagram_found = False

# Вариант 1: По тексту Instagram
try:
    instagram_icon = driver.find_element("xpath", '//android.widget.TextView[@text="Instagram"]')
    instagram_icon.click()
    print("Нашли и кликнули по иконке Instagram (вариант 1)")
    # Вариант 1: По тексту Instagram
    try:
        instagram_icon = driver.find_element("xpath", '//android.widget.TextView[@text="Instagram"]')
        print("Instagram элемент найден!")
        
        # Способ 1: Обычный клик
        try:
            instagram_icon.click()
            print("Обычный клик сработал")
            instagram_found = True
        except:
            print("Обычный клик не сработал, пробуем tap по координатам элемента")
            
            # Способ 2: Получаем координаты элемента и кликаем tap
            location = instagram_icon.location
            size = instagram_icon.size
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            
            driver.tap([(center_x, center_y)], 500)
            print(f"Tap по координатам ({center_x}, {center_y}) выполнен")
            instagram_found = True
            
    except NoSuchElementException:
        print("Вариант 1 не сработал")

    # Если все еще не сработало, попробуем другие методы
    if not instagram_found:
        try:
            instagram_icon = driver.find_element("xpath", '//android.widget.TextView[@text="Instagram"]')
            
            # Способ 3: Используем TouchAction (более надежный для некоторых устройств)
            action = TouchAction(driver)
            action.tap(instagram_icon).perform()
            print("TouchAction клик выполнен")
            instagram_found = True
            
        except Exception as e:
            print(f"TouchAction не сработал: {e}")

    # Способ 4: Если ничего не помогает, попробуем найти родительский элемент
    if not instagram_found:
        try:
            # Ищем родительский контейнер иконки
            instagram_container = driver.find_element("xpath", '//android.widget.TextView[@text="Instagram"]/parent::*')
            instagram_container.click()
            print("Клик по родительскому элементу выполнен")
            instagram_found = True
        except Exception as e:
            print(f"Клик по родительскому элементу не сработал: {e}")

    # instagram_found = True
except NoSuchElementException:
    print("Вариант 1 не сработал")

# # Вариант 2: По содержимому текста
# if not instagram_found:
#     try:
#         instagram_icon = driver.find_element("xpath", '//*[contains(@text, "Instagram")]')
#         instagram_icon.click()
#         print("Нашли и кликнули по иконке Instagram (вариант 2)")
#         instagram_found = True
#     except NoSuchElementException:
#         print("Вариант 2 не сработал")

# # Вариант 3: По content-desc
# if not instagram_found:
#     try:
#         instagram_icon = driver.find_element("xpath", '//*[@content-desc="Instagram"]')
#         instagram_icon.click()
#         print("Нашли и кликнули по иконке Instagram (вариант 3)")
#         instagram_found = True
#     except NoSuchElementException:
#         print("Вариант 3 не сработал")

# # Вариант 4: Поиск любого элемента с Instagram
# if not instagram_found:
#     try:
#         instagram_icon = driver.find_element("xpath", '//*[contains(@content-desc, "Instagram") or contains(@text, "Instagram")]')
#         instagram_icon.click()
#         print("Нашли и кликнули по иконке Instagram (вариант 4)")
#         instagram_found = True
#     except NoSuchElementException:
#         print("Вариант 4 не сработал")

# # Если ничего не сработало, выведем все элементы на экране для отладки
# if not instagram_found:
#     print("Instagram не найден. Ищем все доступные элементы...")
#     elements = driver.find_elements("xpath", '//*[@text or @content-desc]')
#     for i, element in enumerate(elements[:20]):  # Показываем первые 20 элементов
#         try:
#             text = element.get_attribute("text") or ""
#             desc = element.get_attribute("content-desc") or ""
#             print(f"Элемент {i}: text='{text}', content-desc='{desc}'")
#         except:
#             pass

# Кликаем по координатам где должен быть Instagram
# Замени координаты на те, где у тебя находится иконка Instagram
# instagram_x = 200  # Замени на нужную координату X
# instagram_y = 500  # Замени на нужную координату Y

# driver.tap([(instagram_x, instagram_y)], 500)  # 500ms длительность тапа
# print(f"Кликнули по координатам ({instagram_x}, {instagram_y})")

sleep(3)  # Ждем загрузки Instagram

driver.quit()