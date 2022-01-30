#### LAN BACKEND API  WITH JWT

### Terminal commands
Note: make sure you have `pip` and `virtualenv` installed.

    Initial installation: make install

    To run test: make tests

    To run application: make run

    To run all commands at once : make all

Make sure to run the initial migration commands to update the database.

    > python manage.py db init

    > python manage.py db migrate --message 'initial database migration'

    > python manage.py db upgrade


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.

### FAQ ####
    'str' object has no attribute 'decode'

    Downgrading PyJWT did the job for me.
    To achieve that, change the corresponding line in your requirements.txt to
    PyJWT==v1.7.1


    Get IP address of visitors using Flask for Python
    https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
    https://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html


    SQLAlchemy advanced features you need to start using
    https://martinheinz.dev/blog/28


    https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy/37134248