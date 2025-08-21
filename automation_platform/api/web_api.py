# Web API
# REST API для управления ботами и статистики


from typing import List
from fastapi import FastAPI, HTTPException
from automation_platform.core.device_manager import get_connected_devices, restart_device, debug_screen_dump
from automation_platform.core.appium_connector import get_driver
from fastapi import Body
app = FastAPI()

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
