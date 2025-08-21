# Web API
# REST API для управления ботами и статистики


from typing import List
from fastapi import FastAPI, HTTPException
from automation_platform.core.device_manager import get_connected_devices, restart_device, debug_screen_dump, get_screen_xml
from automation_platform.core.appium_connector import get_driver
from automation_platform.utils.device_utils import open_app_drawer
from fastapi import Body
from fastapi.responses import Response


app = FastAPI()

@app.get("/devices/{device_id}/screen_xml")
def screen_xml_endpoint(device_id: str):
    """Возвращает XML-дом экрана устройства как текст"""
    try:
        driver = get_driver(device_id)
        xml = get_screen_xml(driver)
        driver.quit()
        return Response(content=xml, media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения screen xml: {e}")


@app.get("/devices/{device_id}/screen_dump")
def screen_dump_endpoint(device_id: str):
    """Возвращает информацию о всех элементах на экране устройства (для дебага)"""
    try:
        driver = get_driver(device_id)
        elements = debug_screen_dump(driver)
        driver.quit()
        return {"device_id": device_id, "elements": elements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения screen dump: {e}")

@app.post("/devices/{device_id}/test_open_app_drawer")
def test_open_app_drawer_endpoint(device_id: str):
    """Тестовый эндпоинт: открывает список приложений на устройстве (home, свайп, поиск)"""
    try:
        driver = get_driver(device_id)
        open_app_drawer(driver)
        driver.quit()
        return {"status": "success", "device_id": device_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения open_app_drawer: {e}")

@app.post("/devices/{device_id}/restart")
def restart_device_endpoint(device_id: str):
    """Перезапускает устройство по ID"""
    success = restart_device(device_id)
    if success:
        return {"status": "restarting", "device_id": device_id}
    else:
        raise HTTPException(status_code=500, detail=f"Не удалось перезапустить устройство {device_id}")

@app.get("/devices", response_model=List[dict])
def devices_endpoint():
    """Возвращает список реально подключённых устройств"""
    return get_connected_devices()
