Monolithic Gitlab
==================

**DISCLAIMER** This application was made for educational
purpose and not suitable for production.

The monolith app is a Flask app and a Celery worker.


How to run the Flask app
------------------------


For this application to work, you need to create a Gitlab Private Token from your account

Make sure you have virtualenv installed, then you can create a
development environment::

    $ virtualenv .
    $ bin/pip install -r requirements.txt
    $ bin/python setup.py develop

You can then run your application with::

    $ bin/python monolith/app.py
    * Running on http://127.0.0.1:5000/

Go to your browser at http://127.0.0.1:5000/ - you can log in with these
credentials:

- email: suser@example.pl
- password: ok

Once you are logged in, click on "Create User" -- this will redirect to site where you can
create your account with your Gitlab Token.

Once logged, you will be able to see your projects from Gitlab.
But for this, we need to ask the Celery worker to fetch them.


How to run the Celery worker
----------------------------

Make sure you have a redis servier running locally on port 6379 then,
open another shell and run::

    $ bin/celery worker -A monolith.background

This will run a celery microservice that can fetch runs.
To invoke it, visit http://127.0.0.1:5000/fetch.

Once the runs are retrieved, you should see your last ten runs
on http://127.0.0.1:5000


