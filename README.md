�������� ������ '�������� �������'
��� �������� ������� �������������� ��������� ������ Django 1.10.4:
Django==1.10.4

```
## ���������

### 1. �������� ������������ ��������� virtualenv

	mkdir /path/workspace
	cd /path/workspace

	python -m venv memoenv

	������ ���������
	memoenv\Scripts\activate


### 2. �������� �������

    cd /path/workspace
    git clone https://github.com/yart2211/django-memo-project memoproject
    cd memoproject

### 3. ����������
	
	��� �������� ���� ����������� ������� � ����������� ���������� ��������� �������
	pip install -r requirements.txt

### 3. ������������� ������

	�������� ���� ������:
	python manage.py migrate

	�������� ��������� ������ (��������� ������� �� ��������):
	python manage.py loaddata defaultdata.json

### 4. �������� ������������, ������� ����� �������� �� ��������� ��������������.  

	python manage.py createsuperuser


### 5. ������

	python manage.py runserver hostname:portnumber

	��������� ��������������:
	http://hostname:portnumber/admin/

	��������� '������ �������'
	http://hostname:portnumber/memo/
