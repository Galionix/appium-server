from time import sleep
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from selenium.webdriver import Remote



# capabilities теперь задаём через AppiumOptions
# options = UiAutomator2Options()
# options.platform_name = "Android"

# # Appium-специфичные возможности (префикс добавляется автоматически)
# options.automation_name = "UiAutomator2"  # или "uiautomator2"
# options.device_name = "MyPhone"  # Может быть любым для локального устройства
# options.app_package = "com.android.settings"
# options.app_activity = ".Settings"
# options.no_reset = True  # Не сбрасывать состояние приложения

capabilities = {
    "platformName": "Android",  # Standard capability
    "appium:automationName": "uiautomator2",  # Note the prefix
    "appium:deviceName": "MyPhone",
    "appium:appPackage": "com.android.settings",
    "appium:appActivity": ".Settings",
    "appium:noReset": True,
    
        # Увеличиваем таймауты
    "appium:androidInstallTimeout": 180000,  # 3 минуты вместо 1
    "appium:adbExecTimeout": 120000,         # Таймаут ADB команд
    "appium:uiautomator2ServerInstallTimeout": 120000,
}

options = UiAutomator2Options().load_capabilities(capabilities)
options.full_reset = False

options.udid = "6d834b8d0421"
# подключение
remote = webdriver.__dict__.get("Remote")  # Получаем Remote из appium.webdriver
# driver = Remote("http://127.0.0.1:4723", options=options)
driver = remote("http://127.0.0.1:4723", options=options)
# driver = webdriver.Remote("http://127.0.0.1:4723", desired_capabilities=capabilities)

sleep(2)

# пример: клик по элементу с текстом Bluetooth
# el = driver.find_element("xpath", '//android.widget.TextView[@text="Bluetooth"]')
# el.click()

# sleep(2)
# driver.quit()

# Пример: находим элемент по тексту и кликаем
try:
    el = driver.find_element("xpath", '	//android.widget.TextView[@resource-id="android:id/title" and @text="Обновление компонентов"]')
    el.click()
except NoSuchElementException:
    print("Элемент 'Обновление компонентов' не найден")

sleep(2)
driver.quit()
