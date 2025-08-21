"""
Утилиты для работы с Instagram через Appium
"""

def check_instagram_feed_opened(driver):
    """
    Проверяем, что Instagram открылся и мы на главной странице фида
    
    Args:
        driver: WebDriver instance от Appium
        
    Returns:
        bool: True если на главной странице Instagram, False в противном случае
    """
    try:
        # Проверяем package name
        current_package = driver.current_package
        print(f"Текущее приложение: {current_package}")
        
        if "instagram" not in current_package.lower():
            print("❌ Instagram не открыт")
            return False
            
        print("✅ Instagram открыт, проверяем главную страницу...")
        
        # Ищем характерный элемент главной страницы - кнопку сообщений
        try:
            # Способ 1: По resource-id (самый надежный)
            inbox_button = driver.find_element("id", "com.instagram.android:id/action_bar_inbox_button")
            print("✅ Найдена кнопка сообщений по ID - мы на главной странице!")
            return True
        except:
            print("Кнопка сообщений не найдена по ID, пробуем другие способы...")
        
        # Способ 2: По xpath с content-desc
        try:
            inbox_button = driver.find_element("xpath", "//android.widget.Button[contains(@content-desc, 'сообщения') or contains(@content-desc, 'непрочитанных')]")
            print("✅ Найдена кнопка сообщений по content-desc - мы на главной странице!")
            return True
        except:
            print("Кнопка сообщений не найдена по content-desc...")
        
        # Способ 3: По координатам (если кнопка есть в этой области)
        try:
            inbox_button = driver.find_element("xpath", "//android.widget.Button[@bounds='[926,78][1058,232]']")
            print("✅ Найдена кнопка сообщений по координатам - мы на главной странице!")
            return True
        except:
            print("Кнопка сообщений не найдена по координатам...")
            
        # Дополнительная проверка - ищем другие элементы главной страницы
        feed_elements = [
            "com.instagram.android:id/action_bar_camera_button",  # Кнопка камеры
            "//android.widget.TextView[@text='Instagram']",  # Логотип
        ]
        
        for element_locator in feed_elements:
            try:
                if element_locator.startswith("com.instagram"):
                    element = driver.find_element("id", element_locator)
                else:
                    element = driver.find_element("xpath", element_locator)
                print(f"✅ Найден элемент главной страницы: {element_locator}")
                return True
            except:
                continue
                
        print("❌ Не удалось найти характерные элементы главной страницы")
        return False
            
    except Exception as e:
        print(f"Ошибка при проверке: {e}")
        return False


def open_instagram_from_home(driver):
    """
    Открывает Instagram с главного экрана телефона
    
    Args:
        driver: WebDriver instance от Appium
        
    Returns:
        bool: True если Instagram успешно открыт на главной странице
    """
    try:
        # Переходим на главный экран
        driver.press_keycode(3)  # KEYCODE_HOME
        print("Перешли на главный экран")
        
        from time import sleep
        sleep(2)
        
        # Ищем все элементы с Instagram
        instagram_elements = driver.find_elements("xpath", '//*[@text="Instagram" or @content-desc="Instagram"]')
        print(f"Найдено {len(instagram_elements)} элементов с Instagram")
        
        if not instagram_elements:
            print("Элементы с Instagram не найдены")
            return False
        
        # Пробуем кликнуть по каждому найденному элементу
        for i, element in enumerate(instagram_elements):
            try:
                text = element.get_attribute("text") or ""
                desc = element.get_attribute("content-desc") or ""
                print(f"Элемент {i}: text='{text}', content-desc='{desc}'")
                
                # Получаем координаты и кликаем
                location = element.location
                size = element.size
                center_x = location['x'] + size['width'] // 2
                center_y = location['y'] + size['height'] // 2
                
                print(f"Кликаем по координатам ({center_x}, {center_y})")
                driver.tap([(center_x, center_y)], 100)
                
                sleep(3)  # Ждем загрузки Instagram
                
                # Проверяем, что мы на главной странице Instagram
                if check_instagram_feed_opened(driver):
                    print("🎉 Успешно! Instagram открыт и мы на главной странице с лентой!")
                    return True
                else:
                    print("Instagram открылся, но не на главной странице. Пробуем следующий элемент...")
                    # Возвращаемся на главный экран для следующей попытки
                    driver.press_keycode(3)
                    sleep(1)
                    
            except Exception as e:
                print(f"Ошибка при клике по элементу {i}: {e}")
                continue
        
        print("❌ Не удалось открыть Instagram на главной странице")
        return False
        
    except Exception as e:
        print(f"Ошибка при открытии Instagram: {e}")
        return False
    
    
# ...existing code...

# def click_on_new_messages(driver):
#     """
#     Ищет индикаторы новых сообщений в списке чатов и кликает по первому найденному чату
    
#     Args:
#         driver: WebDriver instance от Appium
        
#     Returns:
#         bool: True если найден и кликнут чат с новыми сообщениями, False в противном случае
#     """
#     try:
#         print("Ищем индикаторы новых сообщений...")
        
#         # Ищем все элементы с индикаторами новых сообщений
#         new_message_indicators = driver.find_elements(
#             "xpath", 
#             "//android.view.View[@resource-id='com.instagram.android:id/thread_indicator_status_dot']"
#         )
        
#         if not new_message_indicators:
#             print("❌ Индикаторы новых сообщений не найдены")
#             return False
            
#         print(f"✅ Найдено {len(new_message_indicators)} индикаторов новых сообщений")
        
#         # Кликаем по первому найденному чату с новыми сообщениями
#         for i, indicator in enumerate(new_message_indicators):
#             try:
#                 print(f"Обрабатываем индикатор {i + 1}...")
                
#                 # Получаем родительский элемент (чат)
#                 parent_chat = indicator.find_element("xpath", "./..")
                
#                 # Получаем информацию о чате (если возможно)
#                 try:
#                     chat_info = parent_chat.get_attribute("content-desc") or "Неизвестный чат"
#                     print(f"Найден чат с новыми сообщениями: {chat_info}")
#                 except:
#                     print("Найден чат с новыми сообщениями (без дополнительной информации)")

#                 # Кликаем по индикатору (чату)
#                 indicator.click()
#                 print(f"✅ Кликнули по чату с новыми сообщениями!")
                
#                 from time import sleep
#                 sleep(2)  # Ждем загрузки чата
                
#                 return True
                
#             except Exception as e:
#                 print(f"Ошибка при клике по индикатору {i + 1}: {e}")
#                 continue
        
#         print("❌ Не удалось кликнуть ни по одному чату с новыми сообщениями")
#         return False
        
#     except Exception as e:
#         print(f"Ошибка при поиске новых сообщений: {e}")
#         return False


def check_messages_screen_opened(driver):
    """
    Проверяем, что мы находимся на экране сообщений Instagram
    
    Args:
        driver: WebDriver instance от Appium
        
    Returns:
        bool: True если на экране сообщений, False в противном случае
    """
    try:
        # Ищем характерные элементы экрана сообщений
        messages_indicators = [
            "//android.widget.TextView[@text='Сообщения']",
            "//android.widget.TextView[@text='Messages']", 
            "com.instagram.android:id/action_bar_search",  # Кнопка поиска в сообщениях
            "com.instagram.android:id/thread_list_container",  # Контейнер списка чатов
        ]
        
        for indicator in messages_indicators:
            try:
                if indicator.startswith("com.instagram"):
                    element = driver.find_element("id", indicator)
                else:
                    element = driver.find_element("xpath", indicator)
                print(f"✅ Найден элемент экрана сообщений: {indicator}")
                return True
            except:
                continue
                
        print("❌ Не удалось найти характерные элементы экрана сообщений")
        return False
        
    except Exception as e:
        print(f"Ошибка при проверке экрана сообщений: {e}")
        return False

# ...existing code...
# ...existing code...

def click_on_new_messages(driver):
    """
    Ищет индикаторы новых сообщений в контейнерах чатов и кликает по контейнеру чата
    
    Args:
        driver: WebDriver instance от Appium
        
    Returns:
        bool: True если найден и кликнут чат с новыми сообщениями, False в противном случае
    """
    try:
        print("Ищем чаты с новыми сообщениями...")
        
        # Сначала находим все контейнеры чатов
        chat_containers = driver.find_elements(
            "xpath", 
            "//android.widget.Button[@resource-id='com.instagram.android:id/row_inbox_container']"
        )
        
        if not chat_containers:
            print("❌ Контейнеры чатов не найдены")
            return False
            
        print(f"Найдено {len(chat_containers)} чатов")
        
        # Проверяем каждый контейнер на наличие индикатора новых сообщений
        for i, container in enumerate(chat_containers):
            try:
                print(f"Проверяем чат {i + 1}...")
                
                # Ищем индикатор новых сообщений внутри этого контейнера
                try:
                    new_message_dot = container.find_element(
                        "xpath", 
                        ".//android.view.View[@resource-id='com.instagram.android:id/thread_indicator_status_dot']"
                    )
                    
                    # Если индикатор найден, получаем информацию о чате
                    chat_desc = container.get_attribute("content-desc") or "Неизвестный чат"
                    print(f"✅ Найден чат с новыми сообщениями: {chat_desc}")
                    
                    # Кликаем по всему контейнеру чата
                    container.click()
                    print(f"✅ Кликнули по чату с новыми сообщениями!")
                    
                    from time import sleep
                    sleep(3)  # Ждем загрузки чата
                    
                    return True
                    
                except:
                    # В этом контейнере нет индикатора новых сообщений
                    continue
                    
            except Exception as e:
                print(f"Ошибка при проверке чата {i + 1}: {e}")
                continue
        
        print("❌ Чаты с новыми сообщениями не найдены")
        return False
        
    except Exception as e:
        print(f"Ошибка при поиске новых сообщений: {e}")
        return False

# ...existing code...