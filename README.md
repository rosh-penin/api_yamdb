# api_yamdb
### API для базы данных различных произведений.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/rosh-penin/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:
```
cd yatube_api
```
```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Команда для заполнения таблиц контентом из .csv файлов:

```
python manage.py import_csv
```

Загрузит данные из всех разрешенных .csv файлов внутри директории static/data (относительно базовой директории проекта)
Файлы должны иметь определенную структуру.
