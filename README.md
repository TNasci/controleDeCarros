Simple Flask Todo App using SQLAlchemy and SQLite database.

###
Considerations about the project

tip
```
This project was made with SQLite so I left an instance to run the tests, if you want to do it from scratch, you just have to delete the instance folder and do the entire execution process

In the project there is also a folder with the collection with all the routes already configured
```

### Setup
Create project with virtual environment

command
```
. install.sh

This command will install all the necessary stuff to run the project
```

### If the above command does not work

```
$ python3 -m venv venv
```

Activate it
```console
$ . venv/Scripts/activate
```

or on Linux
```console
venv\bin\activate
```

Install packages
```console
venv/Scripts/pip install -r requirements.txt
```

Set environment variables in terminal
```console
$ export FLASK_APP=app.py
```

or on Windows
```console
$ set FLASK_APP=app.py
```

Run the app
```console
$ flask run
```
