## You can run this server by using a virtualenv (it's cleaner)
#### install virtualenv
```sudo easy_install virtualenv```
#### create a virtualenv
```cd ~```
```virtualenv --no-site-packages --python=YOUR_PYTHON_VERSION django```
> NOTE : YOUR_PYTHON_VERSION should be 3.4 or higher :)
#### activate virtualenv
```source ~/django/bin/activate```
## Install the requirements
```pip install -r requirements.txt```
## Install postgresql
```sudo apt-get install postgresql```
## log into postgres
```sudo su - postgres```
## log in psql
```psql```
## create a database
```CREATE DATABASE lugdunumdb WITH PASSWORD ********;```
```CREATE USER lugdunumuser WITH PASSWORD ********;```
```GRANT ALL PRIVILEGES ON DATABASE lugdunumdb TO lugdunumuser```
> NOTE : be sure to set the right user password in Lugdunum_Server/settings.py
## exit
```\q```
```exit```
## Run server
```python manage.py runserver```
> NOTE : be sure that the right python executable is associated with the 'python' command ;)
### deactivate virtualenv when needed
```desactivate```
### apply migrations and run server
```python manage.py migrate```
```python manage.py runserver```
