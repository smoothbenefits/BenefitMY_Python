BenefitMY_Python
================

Please follow the following steps to start the app on your local machine

0. Install coffeescript component. This is for the coffee javascript files
* `sudo npm install -g coffee-script`

1. Install django
* `sudo apt-get install python-psycopg2`
* `pip install django`
* `pip install djangorestframework`
* `pip install django-pipeline`
* `pip install django-email-as-username`
* `pip install django-encrypted-fields`

1.1. Install required pacakges through npm
* `npm install`

1.2 (optional) if you want to run karma tests easily, you can install karma-cli
* `npm install -g karma-cli`

2. Install postgres

3. Create DB "Benefits_DB"
* `user: "postgres"`
* `password: ""`

4. Get into the src directory
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python syncdb`

5. Load default test data
* `python manage.py loaddata app/fixtures/*.json`

6. Make sure you reset the user table id sequence to be the latest in psql
* `SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));`

7. Collect the static files into the correct staticfiles folder
* `python manage.py collectstatic`

8. Start django server
* `python manage.py runserver`

9. Test api in your web browser by
* `http://localhost:8000/api/v1/people/1/`

10. After each update, run through the following commands:
* `pip install -r`


# Heroku deployment instruction

1. You need to merge all the code from master to branch environment-setup.
This is because: environment-setup branch has the database reference to the db in heroku. While on master, we only have db config referencing our local database. Also, environment-setup branch contains database migration files needed for creating proper migration scripts. Furthermore, heroku environment currently do not support SASS.

2. After the code is merged, you have to run this. This would compile all the .css.scss to .css.css files.
> `sass --update ./app/static/stylesheets/`


3. Go to ./smoothbenefits/settings.py, make sure you replace all .css.scss files to .css.css files. Make sure this is definitely done. Otherwise when deploying heroku, the automatically run  “python manage.py collectstatic” will fail

4. run “python manage.py makemigrations” to generate the migration files. Make sure you check these new migration files in. As you can see on this branch, the .gitignore file do not contain migration files like the .gitignore file on master do.

5. deploy to heroku from the “environment-setup” branch For example: “git push heroku environment-setup:master” if your remote heroku branch is called “heroku”

6. run “heroku run python manage.py migrate” to migrate the changes in model into database

7. run "heroku run python manage.py shell". In shell, run the following commands and confirm in the database usernames have been hashed.
> `from emailusernames.utils import migrate_usernames`
> `migrate_usernames()`

7. Then try to hit the heroku app. If it is not working, run “heroku logs” to see what is the logging on heroku say.

# Run unit tests
1. You can run unit tests by simply do "python manage.py test"
2. However, the above method is slow. You can leverage the pytest package to speed up your unit test run
3. To test with py.test, go to the project root and just do "py.test app/"
4. If the database was not created or you had new migration, please run your test with "py.test --create-db app/"
5. You can also run the tests on multiple threads to speed it up even more. Do "py.test -n <num_of_threads> app/" to do multi-thread testing
6. Again, if the test db needs to be regenerated, you can do "py.test -n <num_of_threads> --create-db app/"
