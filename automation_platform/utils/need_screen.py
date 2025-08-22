from typing import Callable, Dict, Optional, TypedDict
from typing import Mapping

ScreenTransitions = Dict[str, Optional[Callable]]

class ScreenDef(TypedDict):
    resourceId: str
    desc: str
    check: Optional[Callable[[str], bool]]
    transitions: ScreenTransitions

ScreenDict = Mapping[str, ScreenDef]
def need_screen(driver, SCREEN_DICT: ScreenDict, target_screen_name: str, max_transitions: int = 2) -> bool:
    """
    Валидирует, что мы на нужном экране. Если нет — ищет текущий экран, вызывает переход, повторяет проверку.
    Если переход невозможен — кидает ошибку.
    """
    for attempt in range(max_transitions + 1):
        print(f"Attempt {attempt + 1} to reach screen '{target_screen_name}'")
        # 1. Определяем текущий экран
        current_screen = None
        for name, info in SCREEN_DICT.items():
            check = info.get('check')
            if check and check(driver.page_source):
                print(f"Current screen is '{name}'")
                current_screen = name
                break
        # 2. Если уже на нужном экране — успех
        if current_screen == target_screen_name:
            print(f"Already on screen '{target_screen_name}'")
            return True
        # 3. Если не удалось определить текущий экран — ошибка
        if current_screen is None:
            raise RuntimeError("Cannot determine current screen for transition")
        # 4. Если можем перейти — вызываем функцию перехода
        transitions = SCREEN_DICT[current_screen].get('transitions', {})
        transition_func = transitions.get(f'to_{target_screen_name}')
        if callable(transition_func):
            print(f"Transitioning from '{current_screen}' to '{target_screen_name}'")
            success = transition_func(driver)
            print(f"Transition successful: {success}")
            if not success:
                raise RuntimeError(f"Transition from '{current_screen}' to '{target_screen_name}' failed")
        else:
            raise RuntimeError(f"Cannot transition from '{current_screen}' to '{target_screen_name}'")
    # Если не удалось попасть на нужный экран
    raise RuntimeError(f"Failed to reach '{target_screen_name}' after {max_transitions} transitions")