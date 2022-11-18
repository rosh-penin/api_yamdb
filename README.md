# api_yamdb
api_yamdb
New command:
```sh
python manage.py import_csv
```
Will load all allowed .csv files from static/data directory (relative to django project base dir)





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
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

cd yatube_api

Выполнить миграции:

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