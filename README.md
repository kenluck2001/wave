The creation of a spreadsheet reader and showing the summary of the data. The python package manager, pip was the default choice used in this project.


# File Structure

command.py  ( single point for running the web application)         
server.py  ( the core of the web application )
/templates (all the html content) 
    base.html  
    index.html 
    showtable.html
/upload   (folder for saving uploaded file)
CSVFile.py   (class for managing CSV)
models.py     (data models)
requirements.txt  
/static (serving static contents like images, css, javascript)
    /css 
        bootstrap.css  
        dragtable-default.css  
        /icons  
        jquery-ui.css
 
    /fonts 
    /img  
    /js 
        bootstrap.js      
        jquery.dragtable.js  
        jquery-ui.min.js
        jquery-1.10.0.js  
        jquery.tablednd.js   
        notify.js
 
    /script  
        added.js
    /style
        fashion.css



The CSV was validated before uploading to the server. The code was very pythonic as care was taken to simplify the logic.

The order of the column in the spreadsheet can be dragged and drop to allow for viewing two columns in juxtaposition.

The order of the row can be moved to allow for comparisons of two or more row. This reordering is only in the visual space as the ordering of the data in the database is not affected.

The notification to provide feedbacks for the action taken by the user is done to enhance the interface. The user can upload multiple csv files and see the rendered output on the screen. This made extensive use of the flushing in flash framework.

The windows showing the information are based on a collapsible accordion, so the user can focus on the portion of the screen to analyze.

# Installation
The following packages are required to power the web application.


install flask
This is a light weight web framework for serving HTTP
$ pip install Flask
Check ( http://flask.pocoo.org/docs/0.11/installation/ ).

install SQLAlchemy
This is an ORM provides connection with the database.
$ pip install SQLAlchemy
Check ( http://docs.sqlalchemy.org/en/latest/intro.html ).

install csvvalidator
This is for validating the csv file.
$ git clone git://github.com/alimanfoo/csvvalidator.git
$ cd csvvalidator
$ python setup.py install
Check (https://pypi.python.org/pypi/csvvalidator)


install pandas
This allows for managing time series data and for managing dataframe with an intuitive API design.

$ pip install pandas

install mysql and set the connection in the application.

in the client side, I made extensive use of Twitter bootstrap (http://getbootstrap.com/2.3.2/). jQuery library was used for interaction which consist of ( jquery-ui.min.js, jquery-1.10.0.js  ) and the dragging and dropping of the table both for column wise and row wise using (jquery.dragtable.js , jquery.tablednd.js ). The notification system is powered using notify.js on the client side and flask flashing in the server side.

         

# How to use the software
Add the credentials for accessing AWS in the config and credentials file in the settings folder.


To start the web server, navigate to the root of the application and run the command
$ python command.py

To view the page
Enter in the browser (http://127.0.0.1:5000/index)

# Limitations
There is no progress bar for file upload. There will be available in a future version of the software.

# References
https://akottr.github.io/dragtable/

https://github.com/isocra/TableDnD/tree/master/js

https://notifyjs.com/
