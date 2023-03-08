paleocore
==================

Instructions for installing and using Paleo Core for the PSR database locally

Installation
------------------
* Install PyCharm
* Install Postgres.app/PostgreSQL, DBVis and PGAdmin
  * For Mac: easiest way is to use Homebrew
  * For PC: 
  * https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/

* Clone repository from GitHub
```
git clone https://github.com/cocoemily/paleocore2.git paleocore
```
* Open newly created folder with PyCharm
* Create virtual Python environment in PyCharm 
    * https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html


* In the terminal window in PyCharm, run the following code to install the necessary Python libraries for running Paleo Core.
```
pip install -r requirements/dev.txt
```

* In the terminal window, create the database. 
    * This command assumes the database software is installed (see above). The default database for this project uses postgreSQL.
```
createdb paleocore2
```

* From the Tools menu in PyCharm, select "Run manage.py Tasks." This will open a manage.py@paleocore window. 
* In the manage.py@paleocore window, make migrations.
```
migrate
```

Run Server
--------------------
* From the Tools menu in PyCharm, select "Run manage.py Tasks." This will open a manage.py@paleocore window. 
* Create superuser by running the following command and inputting your desired username and password.
```
createsuperuser
```

* Run server on local host.
```
runserver localhost:8000
```

* Open localhost:8000/django-admin/psr in a web browswer.


Importing Data
--------------------
#### Importing Excavation Data from Access Database
* Run server on local host
* Open PSR Excavated Occurrence
* Click "Import New Dataset" button in upper right corner
* Choose a .mdb file to upload
* Click "Upload"

After upload is clicked, the server should display all of the data that you just imported.

#### Importing Survey Data from Shapefile
* Run server on local host
* Choose which type of data to be imported
  * If importing from the _Cave/Rockshelter_ or _Loess Profile_ forms, import from the Geological Context page
  * If importing from the _Archaeology_, _Biology_, _Geology_, or _Aggregate_ forms, import from the PSR Survey Occurrence page
* Click "Import New Dataset" button in upper right corner
* Choose folder that contains the .shp, .dbf and photos from GISPro
* Click "Upload"

After upload is clicked, the server should display all of the data that you just imported. 


Exporting Data
--------------------
#### Exporting Selected Data as CSV
* Run server on local host
* Choose what type of data to exported
* Select items to export
* Select "Export simple report to csv" and click go

#### Exporting Selected Data as Shapefile
* Run server on local host
* Choose what type of data to exported (for now, either Geological Contexts or Survey Occurrences)
* Select items to export
* Select "Export to shapefile" and click go

This will provide point locations for all previous data that can be used with GISPro.

#### Exporting Photos for Selected Locations
* Run server on local host
* Choose Geological Contexts
* Select items to export
* Select "Export photos" and click go

This will provide a folder with enclosed folders labeled by Geological Context names that can be saved in the iPad files to be accessed easily while on survey.
