# Project for onboarding
Create a catalog using Flask-RESTful API

## Installation:
Create a python environment, then install the dependencies by running command:
```
$ pip install -r requirements.txt
```
The default database is using mysql, so create your own connection on mysql.
Then, in order to create the tables, the application will be using alembic. To setup, first run:
```
$ alembic init alembic
```
This will create an alembic directory to hold migration information and an alembic.ini file. Go to the alembic.ini file, and change
sqlalchemy.url to the url of the database in use. Then, to start an initial migration, do:
```
from models.categories import CategoryModel
from models.items import ItemModel
from models.users import UserModel
from db import db
target_metadata = db.metadata
```
Afterwards, you can create some default category by going to the first version (.py file under versions directory in alembic directory) and in the upgrade function,
add some default category, for example: let category_table = op.create_table('category', sa.Column...), then do:
```
op.bulk_insert(category_table,
               [
                   {'id': 1, 'name': 'Category 1'},
                   {'id': 2, 'name': 'Category 2'},
                   {'id': 3, 'name': 'Category 3'},
               ]
               )
```
Afterwards, run upgrade to create the tables:
```
$ alembic upgrade head
```
Then, change the server information accordingly from the ".cfg" configuration files under config directory. \
Then, set the environment variable ENV to select the running environment, for example:
```
$ $env:ENV = "config\developconfig.cfg"
```
Then, run the application by running command:
```
$ python app.py
```
By default, the server will be started on port 5000 of localhost (e.g. http://127.0.0.1:5000)

## Tests:
In order to run tests, first set the ENV variable to:
```
$env:ENV = "..\config\testconfig.cfg"
```
Then, run the tests by doing:
```
$ python -m pytest tests
```

