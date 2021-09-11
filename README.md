# [Shop](https://bit.ly/3foHBZ0):
This project is a simulation of Digimobile that implemented as SSR and CSR 




![image](https://github.com/Mohammadihpython/Shop-/blob/main/images/Shot%200120.png)
## Installing and Getting Started:

1. Clone project into a directory:

```shell script
git clone https://github.com/Mohammadihpython/shop.git
```
2. Open terminal and go to PostgreSQL with:  

```shell script
sudo -su postgres
```
3. Go to PostgreSQL terminal with:

```shell script
psql
```
4. Create a database with: 

```shell script
create database database_name;
```
5. Create a user with:

```shell script
create user your_usename with encrypted password 'your_password';
```

6. Grant privileges to yourself:

```shell script
grant all privileges on database database_name to your_usename;
```

7. Go to this [website](https://miniwebtool.com/django-secret-key-generator/) and create a secret key:

8 ??

9. create a local_settings.py file and enter local configs there:

local_settings.py:
```shell script
API_KEY = 'your_API_KEY'
SECRET_KEY = 'your_SECRET_KEY'
DEBUG = True/False
DB_NAME = "your_database_name"
DB_USER = "your_database_username"
DB_PASSWORD = "your_database_user+password"
```

10. install requirements of the project:
```shell script
pip install -r requirements.txt
```

11. Migrate the migrations:

first:
```shell script
python manage.py makemigrations
```
then:
```shell script
python manage.py migrate
```
12. Run Celery with:
```shell script
celery -A OnlineWallet worker -l info -P gevent
```
13. Run Server and start use this project:
```shell script
python manage.py runserver
```
## Built With:
* [Django](https://www.djangoproject.com/) - Framework used
* [DRF]
* [javascripts(ajax)]
* [PostgrSQL](https://www.postgresql.org) - Used PostgrSQL database to store data
* [Redis](https://www.redis.io) - Used to queuing tasks
* [Celery](http://www.celeryproject.org/) - Used for asynchronous tasks
