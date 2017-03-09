Тестовый проект 'Менеджер заметок'.

При создании проекта использовалась последняя версия Python 3.5.2, Django 1.10.4:
Django==1.10.4

```
## Установка

### 1. Создание виртуального окружения virtualenv

	mkdir /path/workspace
	cd /path/workspace

	python -m venv memoenv

	Запуск окружения
	memoenv\Scripts\activate


### 2. Загрузка проекта

    cd /path/workspace
    git clone https://github.com/yart2211/django-memo-project memoproject
    cd memoproject

### 3. Требования
	
	Для загрузки всех необходимых модулей и фреймворков необходимо выполнить команду
	pip install -r requirements.txt

### 3. Инициализация данных

	Создание базы данных:
	python manage.py migrate

	Загрузка начальных данных (категории заметок по умочанию):
	python manage.py loaddata defaultdata.json

### 4. Создание пользователя, который может заходить на интерфейс администратора.  

	python manage.py createsuperuser


### 5. Запуск

	python manage.py runserver hostname:portnumber

	Интерфейс администратора:
	http://hostname:portnumber/admin/

	Интрефейс 'Список заметок'
	http://hostname:portnumber/memo/
