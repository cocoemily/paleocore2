paleocore
==================

Instructions for installing and using Paleo Core for the PSR database locally

Installation
------------------
* Install PyCharm
* Install Postgres.app, DBVis and PGAdmin
* Fork repository from paleocore/paleocore2 on GitHub

* Clone repository from GitHub and move into that directory
```
git clone https://github.com/<your_username>/paleocore2.git paleocore
cd paleocore
```

* Create virtual Python environment
```
virtualenv -p python3 venv
```

* Start the virtual environment and install the python libraries stipulated in the requirements file. Separate files stipulate a base set of libraries which are imported into dev and production requirement files.
```
source venv/bin/activate
pip install -r requirements/dev.txt
```

* Create the database. Assuming the database software is installed. The default database for this project uses postgreSQL. The simplest method of implementing the database is using postgres.app.
```
createdb paleocore2
```

* Run migrations.
```
manage.py migrate
```

Run Server
--------------------
* Start virtual environment.

* Create superuser.
```
manage.py createsuperuser
```

* Run server on local host.
```
manage.py runserver localhost:8000
```

* Open localhost:8000/django-admin/psr in a web browswer.


Importing Data
--------------------
#### Importing Excavated Objects from Access Database
* Run server on local host
* Open PSR Excavated Occurrence
* Click "Import New Dataset" button in upper right corner
* Choose a .mdb file to upload
* Click "Upload"


#### Importing Survey Occurrences from Shapefile
* Run server on local host
* Choose which type of data to be imported
* Click "Import New Dataset" button in upper right corner
* Choose a .shp file to upload
* Click "Upload"


Exporting Data
--------------------
#### Exporting Selected Data
* Run server on local host
* Choose what type of data to exported
* Select items to export
* Select "Export simple report to csv" and click go
