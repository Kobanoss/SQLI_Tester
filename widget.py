import sys
import time

# Импорт библиотеки для слепого time-based тестирования
from Blinder.blinder import blinder

# Импорт библиотеки для валидации URl
from validator_collection import checkers

# Импорт модуля, который в последствии используется для проверки доступности URL
import urllib.request

# Импорт библиотек для QT (GUI)
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

from forms.ui_widget import Ui_Widget

# Импорт самописного модуля для error-based тестирования
from custom_testers.errors_sqli import scan_sql_injection as errors_scan


class Widget(QWidget):
    def __init__(self, output_file: str = ''):
        super(Widget, self).__init__()
        self.__ui = Ui_Widget()
        self.__ui.setupUi(self)

        # Задание основных атрибутов класса
        self.__url: str
        self.__type: str
        self.__feedback: bool
        self.__output_file = output_file

        # Задание связей между сигналами и слотами (реакция в лице метода класса на изменение состояния объекта)
        self.__ui.pushButton_Error.pressed.connect(self.__disable_clickble_objects)
        self.__ui.pushButton_Time.pressed.connect(self.__disable_clickble_objects)

        self.__ui.pushButton_Error.pressed.connect(self.__error_based_check)
        self.__ui.pushButton_Time.pressed.connect(self.__time_based_check)

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
        self.__ui.pushButton_Time.setEnabled(False)
        self.__ui.pushButton_Error.setEnabled(False)

    def __enable_clickble_objects(self) -> None:
        self.__ui.lineEdit_Url.setEnabled(True)
        self.__ui.pushButton_Time.setEnabled(True)
        self.__ui.pushButton_Error.setEnabled(True)

    # Выгрузка результатов в файл (Задается програмно в блоке main)
    def __send_data_to_file(self) -> None:
        with open(file=self.__output_file, mode='a+', encoding='utf-8') as file:
            feedback = f"[{'Vulnerable' if (self.__feedback is not None) else 'Clear'}]"
            file.write(f"{feedback:>12} >> {self.__type:>13} >> {self.__url}\n")

    # Восстановка формами стандартного значения
    def __reset_forms(self) -> None:
        self.__set_label_Status('')

    def __validate_url(self) -> False or str:
        self.__url = self.__ui.lineEdit_Url.text()
        if not checkers.is_url(self.__url):
            self.__set_label_Status("Bad URL")
            self.__enable_clickble_objects()
            return False

        if not self.__check_connection_url():
            self.__set_label_Status("Can't reach this URL")
            self.__enable_clickble_objects()
            return False

        return self.__url

    def __check_connection_url(self) -> bool:
        try:
            urllib.request.urlopen(self.__url).getcode()
        except BaseException:
            return False
        return True

    # Вызов методов из самописного модуля для error-based тестирования с предварительной валидацией URL
    def __error_based_check(self) -> None:
        self.__url = self.__validate_url()
        if self.__url is False:
            return

        self.__type = "[Error-based]"
        self.__set_label_Status("Started Error-based SQL Injection check")
        self.__set_progress_bar(5)

        status = errors_scan(self.__url)
        self.__set_label_Status("URL clear" if status is False else "URL can be injected")
        self.__set_progress_bar(100)
        self.__feedback = status
        self.__send_data_to_file()

        time.sleep(2)
        self.__set_progress_bar(0)
        self.__enable_clickble_objects()

    # Вызов метода из подгружаемой библиотеки для time-based тестирования с предварительной валидацией URL
    def __time_based_check(self) -> None:
        self.__url = self.__validate_url()
        if self.__url is False:
            return

        self.__type = "[Time-based]"
        self.__set_label_Status("Started Time-based SQL Injection check")
        self.__set_progress_bar(5)

        blind = blinder(self.__url, sleep=0.5)
        status = blind.check_injection()

        self.__set_label_Status("URL clear" if status is False else "URL can be injected")
        self.__set_progress_bar(100)
        self.__feedback = status
        self.__send_data_to_file()

        time.sleep(2)
        self.__set_progress_bar(0)
        self.__enable_clickble_objects()


# Основная функция -> Запуск окна
def main() -> None:
    app = QApplication(sys.argv)

    window = Widget(output_file="./log.txt")

    window.setWindowIcon(QIcon("./src/logo.jpg"))
    window.setWindowTitle("SQLI Tester")

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
