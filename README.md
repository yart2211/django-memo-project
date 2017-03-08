При создании проекта использовалась последняя версия Django 1.10.4:
Django==1.10.4

```
## Установка

### 1. Создание виртуального окружения virtualenv

	mkdir /path/workspace
	cd /path/workspace

	python -m venv myenv


### 2. Загрузка проекта

    cd /path/to/your/workspace
    $ git clone git://github.com/kirpit/django-sample-app.git projectname && cd projectname

### 3. Требования
	
	Для загрузки всех необходимых модулей и фреймворков необходимо выполнить команду
	pip install -r requirements.txt

### 3. Создание пользователя, который может заходить на интерфейс администратора.  

	python manage.py createsuperuser

### 4. Инициализация данных

	Создание базы данных:
	python manage.py migrate

	Загрузка начальных данных (категории заметок по умочанию):
	python manage.py loaddata defaultdata.json

### 5. Запуск
	python manage.py runserver

	Интерфейс администратора:
	http://localhost:8000/admin/

	Интрефейс 'Список заметок'
	http://localhost:8000/memo/
