import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Set
from urllib.parse import urljoin
import bs4.element
from bs4 import BeautifulSoup as bs

# Инициализируем HTTP сессию
s = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)

s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" \
                          "83.0.4103.106 Safari/537.36"


def get_all_forms(url: str) -> bs4.element.ResultSet:
    """
    Функция, использующая BeautifulSoup на request c данного URL
    для получения всех имеющихся форм.

    :param  url: Строка, являющаяся URL сайта.
    :return: ResultSet со всеми формами.
    :rtype: bs4.element.ResultSet
    """

    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form: bs4.element.Tag) -> dict:
    """ 
    Данная функция, всю возможную полезную информацию
    о предоставленной HTML форме.

    :param  form: HTML форма типа Tag, который является элементом ResultSet.
    :return: Словарь с полученными из формы данными.
    :rtype: dict
    """

    details = {}

    # Получаем действие(action) с формы
    try:
        action = form.attrs.get("action").lower()
    except Exception:
        action = None
    except BaseException:
        action = None

    # Получаем метод формы (POST, GET, и т.д.)
    method = form.attrs.get("method", "get").lower()

    # Получаем детали ввода, такие как тип(type) и имя(name)
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    # Объединяем все в один словрь
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def is_vulnerable(response: requests.models.Response) -> bool:
    """
    Простая булевая функция, определяющая, уязвима ли страница
    к SQL инъекции по ее 'ответу'.

    :param  response: Ответ сайта, полученный постредством модуля requests.
    :return: Булевое значение, показывающее уязвимость страницы -> True - уязвима | False - нет
    :rtype: bool
    """

    # TODO: CONNECT XML ERROR RE FILE TO ERRORS

    errors = {
        # ======== PostgreSQL ========
        "ERROR:  syntax error",

        # ========== MySQL ===========
        "You have an error in your SQL",
        "you have an error in your sql syntax;",
        "warning: mysql",
        "MySQL server version for the right syntax",
        "supplied argument is not a valid MySQL result resource",

        # ========= SQLite3 ==========
        "<b>Warning</b>:  SQLite3",
        "unrecognized token:",
        "Unable to prepare statement:",

        # ======== SQL Server ========
        "unclosed quotation mark after the character string",

        # ========= Oracle ===========
        "quoted string not properly terminated",
    }
    # Задаем набор доступных кодировок
    encode_set = (
        'utf_8', 'ascii', 'cp1251', 'utf_16', 'utf_32')
    for encoding in encode_set:
        for error in errors:

            # Возвращаем True при условии получении ошибки
            try:
                if error in response.content.decode(encoding).lower():
                    print(f'{encoding = }')
                    return True
            except Exception:
                continue
            except BaseException:
                continue

    # При отсутствии ошибки
    return False


def scan_sql_injection(url: str) -> None or str:
    """
    Основная функция, осуществляющая вызов проверки SQLI по самому URL и его формам при необходимости.

    :param      url: Строка, являющаяся URL проверяемого сайта.
    :return:    В случае удачного теста на SQLI, возвращает URL сайта, в противном случае возвращает None.
    :rtype:     None or str
    """
    for char in ('\\', '"', "'", '?', '/', '.'):

        # Добавляем 'ошибочные' символы к строке URL
        new_url = f"{url}{char}"
        print("[!] Trying", new_url)

        # Делаем HTTP запрос
        res = s.get(new_url)
        if is_vulnerable(res):
            # Если словили ошибку, значит SQLI допустима -> дальнейшие проверки не требуются,
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            return url
        # Задержка отправки пакетов
        time.sleep(0.2)

    # Если предыдущий пункт не сработал, начинаем тест всех доступных форм
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}")

    for form in forms:
        form_details = get_form_details(form)

        for char in ('\\', '"', "'", '?', '/', '.'):

            # Тело данных, которую мы хотим валидировать
            data = {}

            for input_tag in form_details["inputs"]:
                print(input_tag)

                if input_tag["type"] == "hidden" or input_tag["value"]:

                    # Для любой формы "hidden" или со значением, используем данные с "ошибочным" модификатором
                    try:
                        data[input_tag["name"]] = input_tag["value"] + char
                    except Exception:
                        print('...Wait')
                    except BaseException:
                        print('...Wait')

                elif input_tag["type"] != "submit":

                    # Для всех других, кроме submit'a используем просто "мусорные" данные
                    data[input_tag["name"]] = f"test{char}"

            # Добавляем к URL измененное действие(action)
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)

            # Проверка итоговой страницы на SQLI
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                print(form_details)
                return url, form_details

            # Задержка оправки пакетов
            time.sleep(0.2)


if __name__ == "__main__":
    url_list = ["https://evcppk.ru/article.php?id=140", "http://alvet.ru/v_article.php?id=35",
                "http://www.sfgames.ru/gameS.php?id=284",
                 "http://dveromania.ru/furnitura/bronenakladki",
                "http://www.layayoga.ru/index.php?id=1/",
                "http://mstinfo.ru/catalog/dog.php?id=4234&screen=4&userif=2"
                ]
    try:
        for url in url_list:
            url_is_vulnerable = scan_sql_injection(url)
            print(f"url_is_vulnerable = {url_is_vulnerable}\n")
    except _ as ex:
        print(ex)
