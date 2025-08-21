# ...existing code...

def get_screen_xml(driver):
    """
    Возвращает XML-дом экрана устройства
    """
    try:
        return driver.page_source
    except Exception as e:
        print(f"Ошибка получения XML: {e}")
        return ""
# ...existing code...

def debug_screen_dump(driver):
    """
    Возвращает список всех элементов на экране с их атрибутами для дебага.
    Требует активного Appium driver.
    """
    elements_info = []
    try:
        elements = driver.find_elements("xpath", "//*")
        for el in elements:
            try:
                info = {
                    "class": el.get_attribute("className"),
                    "resource_id": el.get_attribute("resourceId"),
                    "text": el.get_attribute("text"),
                    "content_desc": el.get_attribute("contentDescription"),
                    "bounds": el.get_attribute("bounds"),
                    "displayed": el.is_displayed()
                }
                elements_info.append(info)
            except Exception:
                continue
        return elements_info
    except Exception as e:
        print(f"Ошибка при получении элементов экрана: {e}")
        return []
# ...existing code...

def restart_device(device_id):
    """Перезапускает устройство через adb (adb reboot)"""
    try:
        result = subprocess.run([
            "adb", "-s", device_id, "reboot"
        ], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Ошибка перезапуска устройства {device_id}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Ошибка перезапуска устройства {device_id}: {e}")
        return False
# Device Manager
# Управление подключением и состоянием устройств (Appium)

import subprocess

def get_connected_devices():
    """Получает список подключённых Android-устройств через adb"""
    try:
        result = subprocess.run([
            "adb", "devices"], capture_output=True, text=True
        )
        lines = result.stdout.strip().splitlines()
        devices = []
        for line in lines[1:]:  # Пропускаем первую строку 'List of devices attached'
            if line.strip() and "device" in line:
                device_id = line.split()[0]
                # Получаем модель устройства
                try:
                    model_result = subprocess.run([
                        "adb", "-s", device_id, "shell", "getprop", "ro.product.model"
                    ], capture_output=True, text=True)
                    model = model_result.stdout.strip()
                except Exception:
                    model = "Unknown"
                devices.append({"id": device_id, "name": model, "status": "online"})
        return devices
    except Exception as e:
        print(f"Ошибка получения устройств: {e}")
        return []
# Device Manager
# Управление подключением и состоянием устройств (Appium)
