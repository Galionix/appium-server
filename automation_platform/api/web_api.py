# Web API
# REST API для управления ботами и статистики


from datetime import time
from typing import List
from fastapi import FastAPI, HTTPException
from automation_platform.apps.instagram.test_scenario import test_scenario
from automation_platform.core.device_manager import get_connected_devices, restart_device, debug_screen_dump, get_screen_xml
from automation_platform.core.appium_connector import get_driver
from automation_platform.utils.device_utils import open_app
from fastapi import Body
from fastapi.responses import Response
import time


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

@app.post("/devices/{device_id}/test_scenario")
def test_scenario_endpoint(device_id: str):
    """Тестовый эндпоинт: выполняет тестовый сценарий для Instagram."""
    try:
        driver = get_driver(device_id)
        result = test_scenario(driver)
        driver.quit()
        return {"status": "success", "device_id": device_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения test_scenario: {e}")

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
