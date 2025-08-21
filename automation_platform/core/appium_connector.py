"""
Модуль для подключения к устройству через Appium и получения драйвера
"""
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

# Можно расширить для поддержки нескольких устройств

def get_driver(device_id: str = ""):
    """
    Возвращает Appium driver для устройства
    device_id: уникальный идентификатор устройства (udid)
    """
    capabilities = {
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:deviceName": "MyPhone",
        "appium:noReset": True,
        "appium:fullReset": False,
        "appium:androidInstallTimeout": 180000,
        "appium:adbExecTimeout": 120000,
        "appium:uiautomator2ServerInstallTimeout": 120000,
    }
    options = UiAutomator2Options().load_capabilities(capabilities)
    if device_id:
        options.udid = device_id
    remote = webdriver.__dict__.get("Remote")
    driver = remote("http://127.0.0.1:4723", options=options) # pyright: ignore[reportOptionalCall]
    return driver
