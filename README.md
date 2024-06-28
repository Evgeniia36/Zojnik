Инструкция для запуска тестов на Windows через командную строку
1. Скачать и установить Python с официального сайта [python.org](https://www.python.org/). При установке добавить Python в переменную среды PATH.
2. Скачать проект [Zojnik](https://github.com/Evgeniia36/Zojnik/tree/main) на локальный компьютер и распаковать в папку Zojnik
3. В коммандной строке перейти в папку Zojnik, создать и активировать виртуальное окружение:
   
   `python -m venv venv`
   
   `venv\Scripts\activate`
4. Установить зависимости из файла requirements.txt: В коммандной строке перейти в папку, содержащую файл requirements.txt (скорее всего, вы уже там), далее выполнить команду:
   
   `pip install -r requirements.txt`
5. Запустить тесты:
   
   `pytest`
