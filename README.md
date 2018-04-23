## Install the requirements
```pip install -r requirements.txt```
## Run server
```python manage.py runserver```
> NOTE : be sure that the right python executable is associated with the 'python' command ;)
## You can run this server by using a virtualenv.
### install virtualenv
```sudo easy_install virtualenv```
### create a virtualenv
```cd ~```
```virtualenv --no-site-packages --python=YOUR_PYTHON_VERSION django```
> NOTE : YOUR_PYTHON_VERSION should be 3.4 or higher :)
### activate virtualenv
```source ~/django/bin/activate```
### deactivate virtualenv when needed
```desactivate```