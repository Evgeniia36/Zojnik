Инструкция для запуска тестов на Windows через командную строку
1. Скачать и установить Python с официального сайта [python.org](https://www.python.org/). При установке добавить Python в переменную среды PATH.
2. В коммандной строке создать и активировать виртуальное окружение:
   `python -m venv venv` 
   `venv\Scripts\activate`
3. Скачать файл requirements.txt на локальный компьютер
4. Установить зависимости из файла requirements.txt: В коммандной строке перейти в папку, содержащую файл requirements.txt, далее выполнить команду:
   `pip install -r requirements.txt`
5. Запустить тесты:
   `pytest`
