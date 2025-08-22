from appium.webdriver.common.touch_action import TouchAction
import math
import random

def swipe_arc(driver, start, end, radius=300, steps=10, duration=800):
    """
    Свайп по дуге между двумя точками.
    start, end: (x, y)
    radius: радиус дуги (относительно центра между точками)
    steps: количество промежуточных точек
    duration: общая длительность свайпа (мс)
    """
    x0, y0 = start
    x1, y1 = end
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2  # центр дуги

    # угол между точками
    angle0 = math.atan2(y0 - cy, x0 - cx)
    angle1 = math.atan2(y1 - cy, x1 - cx)

    # генерируем точки по дуге
    points = []
    for i in range(steps + 1):
        t = i / steps
        angle = angle0 + (angle1 - angle0) * t
        x = int(cx + radius * math.cos(angle))
        y = int(cy + radius * math.sin(angle))
        # добавляем небольшую рандомизацию
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)
        points.append((x, y))

    action = TouchAction(driver)
    action.press(x=points[0][0], y=points[0][1])
    for x, y in points[1:]:
        action.move_to(x=x, y=y)
    action.release()
    action.perform()