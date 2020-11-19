
*Flask allows you to register environment variables that you want to be automatically imported when you run the flask command.*

* `pip install python-dotenv`

Then you can just write the environment variable name and value in a .flaskenv file in the top-level directory of the project:

    root/
    .flaskenv
        FLASK_APP=main.py

# Things To Do
* create a route `/auth` to organize views of authentications instead of call it in index page.