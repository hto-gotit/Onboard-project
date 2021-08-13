# Project for onboarding
Create a catalog using Flask-RESTful API

## Installation:
Create a python environment, then install the dependencies by running command:
```
$ pip install -r requirements.txt
```
The default database is using mysql, so create your own connection on mysql, and create a database. Then, change the server information accordingly 
in app.py at app.config [SQLALCHEMY_DATABASE_URI]. \
Then, run the application by running command:
```
$ python app.py
```
By default, the server will be started on port 5000 of localhost (e.g. http://127.0.0.1:5000)

## Tests:
In order to run tests, first run the application, then run command:
```
$ python -m pytest tests
```

