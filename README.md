# Система прогнозирования и анализа курса криптовалют

Первый этап работы над проектом является поисковой работой.
Планируется изучить различные средства для прогнозирования временных рядов,
а также разработать алгоритм поиска фигур технического анализа.

Предполагается два интерфейса для работы с пользователем. PyQt5 приложение и телеграмм-бот.
Телеграмм-бот появится на заключительном этапе реализации проекта для демострации.

## Установка на Linux

Установить Python версии 3.10 (см. [инструкцию](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux))

Создать виртуальное окружение

``` bash
python3 -m venv .venv
```

Активизировать виртуальное окружение

``` bash
source .venv/bin/activate
```

Установить зависимости

``` bash
python3 -m pip install -r requirements.txt
```

или (для минимального количества зависимостей):

``` bash
python3 -m pip install -r req_needed.txt
```

## Запуск

``` bash
python3 main.py
```
