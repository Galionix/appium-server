1. Минимальный вариант — через ADB
Если телефон подключён к ПК по USB и включён режим USB debugging, ты можешь уже сейчас управлять им.

Запустить приложение

bash
Копіювати
Редагувати
adb shell monkey -p com.package.name 1
где com.package.name — пакет нужного приложения.

Сымитировать нажатия

bash
Копіювати
Редагувати
adb shell input tap X Y
adb shell input swipe X1 Y1 X2 Y2 500
adb shell input text "Hello"
Сделать скриншот

bash
Копіювати
Редагувати
adb exec-out screencap -p > screen.png
Получить дерево UI (чтобы узнать, какие элементы на экране)
Ставишь uiautomator:

bash
Копіювати
Редагувати
adb shell uiautomator dump /sdcard/view.xml
adb pull /sdcard/view.xml .
В файле будет структура всех элементов.

Минус: всё это "низкоуровневое" и придется вручную обрабатывать координаты и XML.

2. Более высокий уровень — Appium
Appium — фреймворк, который может управлять Android как "виртуальный палец":

Запускает приложения.

Находит элементы по ID, тексту, XPath.

Делает скриншоты.

Работает через ПК, подключённый к устройству по USB или Wi-Fi.

Пример на Python:

python
Копіювати
Редагувати
from appium import webdriver

caps = {
    "platformName": "Android",
    "deviceName": "MyPhone",
    "appPackage": "com.package.name",
    "appActivity": "MainActivity",
    "automationName": "UiAutomator2"
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
driver.find_element_by_accessibility_id("Login").click()
driver.quit()
Плюс: не нужно самому разбирать XML, можно сразу искать по имени или ID элемента.
Минус: нужно поднять Appium сервер и разобраться с настройкой.

3. Гибкий "пишем свой тул"
Ты можешь написать собственный софт, который:

По USB общается с телефоном через ADB (есть Python-библиотеки pure-python-adb, adbutils).

Делает скриншоты и парсит их через OCR (например, tesseract) для распознавания текста.

Получает XML из uiautomator для точной информации о кнопках.

Посылает команды input tap/swipe.

Это уже будет полноценный бот, но UI-аналитику (что на экране и что активно) придётся либо брать из uiautomator, либо самому распознавать.

4. Если нужен полный доступ к экрану в реальном времени
Тогда можно использовать:

scrcpy — трансляция экрана + ввод с ПК.

Снять поток с adb exec-out screenrecord.

Для автоматизации можно встраивать scrcpy в Python-скрипт, отправляя команды через ADB.

💡 Если тебе нужен прямо "смарт" сценарий:

На ПК будет Python-скрипт.

Он по USB подключается к телефону (ADB).

Через uiautomator получает дерево элементов.

Выбирает нужный элемент (по тексту, ID).

Делает adb shell input tap по его координатам.

Всё это можно автоматизировать под любой сценарий.

Я могу тебе расписать инструкцию, как поднять Appium + UiAutomator2 для Windows, чтобы ты прямо с компьютера мог:

Запускать приложение по имени пакета.

Читать структуру элементов.

Кликать по ним без вычисления координат.

Получать скриншоты.

Это будет куда удобнее, чем вручную на ADB.

Хочешь, чтобы я сделал такой пошаговый гайд?








Ви сказали:
да давай гайд, звучит круто и просто!


Програма ChatGPT сказала:
Окей, тогда сделаем тебе рабочий набор для полного управления Android с ПК через Appium + UiAutomator2 на Windows, чтобы можно было и запускать приложения, и кликать по элементам, и получать инфу о том, что на экране.

🚀 Часть 1 — Подготовка телефона
Включи режим разработчика

Настройки → О телефоне → 7 раз тапни по "Номер сборки".

Включи отладку по USB

Настройки → Для разработчиков → "USB debugging" (и по желанию — "Install via USB").

Подключи телефон к ПК по кабелю → при первом подключении на телефоне разреши отладку.

⚙️ Часть 2 — Установка инструментов на Windows
Java

Скачай Java 17 JDK и установи.

В Параметры → Система → О системе → Доп. параметры → Переменные среды добавь в PATH:

makefile
Копіювати
Редагувати
C:\Program Files\Eclipse Adoptium\jdk-17\bin
В консоли проверь:

bash
Копіювати
Редагувати
java -version
Android SDK Platform Tools

Скачай platform-tools.

Распакуй, положи куда удобно, путь добавь в PATH.

Проверь:

bash
Копіювати
Редагувати
adb devices
Должен появиться твой телефон.

Node.js

Скачай LTS-версию с nodejs.org.

Appium
Устанавливаем глобально:

bash
Копіювати
Редагувати
npm install -g appium
Проверка:

bash
Копіювати
Редагувати
appium --version
Appium drivers
Установим UiAutomator2:

bash
Копіювати
Редагувати
appium driver install uiautomator2
📦 Часть 3 — Python-окружение
Установи Python 3.10+.

Создай папку проекта и активируй виртуальное окружение:

bash
Копіювати
Редагувати
python -m venv venv
venv\Scripts\activate
Поставь Appium клиент:

bash
Копіювати
Редагувати
pip install Appium-Python-Client
▶️ Часть 4 — Запуск Appium сервера
В отдельной консоли просто запусти:

bash
Копіювати
Редагувати
appium
Если всё ок, он напишет, что сервер слушает 0.0.0.0:4723.

🖥 Часть 5 — Пробный скрипт
Создаём test.py:

python
Копіювати
Редагувати
from appium import webdriver
from time import sleep

caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "MyPhone",
    "appPackage": "com.android.settings",  # Пакет приложения
    "appActivity": ".Settings",           # Активити для запуска
    "noReset": True
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

sleep(2)

# Пример: находим элемент по тексту и кликаем
el = driver.find_element("xpath", '//android.widget.TextView[@text="Bluetooth"]')
el.click()

sleep(2)
driver.quit()
Запусти:

bash
Копіювати
Редагувати
python test.py
Телефон откроет настройки и нажмёт на "Bluetooth".

🛠 Часть 6 — Как находить элементы
Поставь Appium Inspector:

Скачать здесь

Это GUI, который показывает структуру UI в реальном времени.

Запусти Inspector, подключи к http://localhost:4723/wd/hub, укажи capabilities (appPackage, appActivity, deviceName).

Наводи курсор на элементы → получай их ID, XPath, текст.

📌 Итого
После этой настройки ты сможешь:

Запускать любое приложение по package/activity.

Находить элементы по ID, тексту, XPath.

Получать скриншоты:

python
Копіювати
Редагувати
driver.save_screenshot("screen.png")
Считывать текст с экрана через OCR (если надо).

Автоматизировать любые действия.

Если хочешь, я могу тебе собрать шаблон Python-бота для Android, который:

Сам подключается к телефону.

Умеет искать элементы по тексту/ID.

Делает скриншоты и логирует найденные элементы.

Так тебе будет не нужно писать всё с нуля, только подставлять свои действия.
Хочешь, сделаем такой готовый скелет?

"Remote" is not exported from module "appium.webdriver"PylancereportPrivateImportUsage
class Remote(
    command_executor: str | AppiumConnection = 'http://127.0.0.1:4723',
    extensions: List[type[ExtensionBase]] | None = None,
    options: AppiumOptions | List[AppiumOptions] | None = None,
    client_config: AppiumClientConfig | None = None
)
Create a new driver that will issue commands using the wire protocol.


Argument of type "dict[str, Unknown]" cannot be assigned to parameter "extensions" of type "List[type[ExtensionBase]] | None" in function "__init__"
  Type "dict[str, Unknown]" is not assignable to type "List[type[ExtensionBase]] | None"
    "dict[str, Unknown]" is not assignable to "List[type[ExtensionBase]]"
    "dict[str, Unknown]" is not assignable to "None"PylancereportArgumentType
(variable) caps: dict[str, Unknown]




Програма ChatGPT сказала:
Да, это потому что в новых версиях Appium-Python-Client убрали старый способ подключения через

python
Копіювати
Редагувати
from appium import webdriver
driver = webdriver.Remote("url", caps)
и теперь нужно использовать AppiumOptions вместо простого dict для capabilities.

Вот как твой пример переписать под новый API:
python
Копіювати
Редагувати
from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep

# capabilities теперь задаём через AppiumOptions
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "MyPhone"
options.app_package = "com.android.settings"
options.app_activity = ".Settings"
options.no_reset = True

# подключение
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

sleep(2)

# пример: клик по элементу с текстом Bluetooth
el = driver.find_element("xpath", '//android.widget.TextView[@text="Bluetooth"]')
el.click()

sleep(2)
driver.quit()
Что изменилось:
Вместо caps = { ... } теперь:

python
Копіювати
Редагувати
from appium.options.android import UiAutomator2Options
options = UiAutomator2Options()
options.app_package = "..."
webdriver.Remote теперь принимает options=options, а не словарь capabilities.

Адрес сервера можно писать без /wd/hub, он по умолчанию 4723.