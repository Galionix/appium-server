import xml.etree.ElementTree as ET

def count_new_dm_requests(xml_str: str) -> int:
    """
    Возвращает количество новых запросов в директ Instagram по XML.
    Ищет вкладку 'Запросы' с числом >0.
    """
    try:
        root = ET.fromstring(xml_str)
        for elem in root.iter():
            # Ищем TextView или Button с текстом вида 'Запросы N', где N > 0
            text = elem.attrib.get('text', '')
            if text.startswith('cЗапросы'):
                # В тексте после 'cЗапросы' может быть пробел и число
                parts = text.split()
                if len(parts) == 2 and parts[1].isdigit():
                    if int(parts[1]) > 0:
                        return int(parts[1])
        return 0
    except Exception:
        return 0
