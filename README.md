BenefitMY_Python
================
### Setup your development environment
Please follow the following steps to start the app on your local machine

* Setup the virtual environment. Make sure you downloaded and installed the virtual environment wrapper tool (https://virtualenvwrapper.readthedocs.org/en/latest/)
* ```sh
  $ mkvirtualenv benefitmy
  ```
* Make sure you have npm installed
* ```sh
  $ sudo apt-get install npm
  ```
* Install postgres (http://www.postgresql.org/download/macosx/) and then Create DB "Benefits_DB"
* ```sh
  $ createuser postgres
  $ createdb -O postgres -w Benefits_DB
  ```

* Pip install
* ```sh
  $ pip install -r requirements.txt
  ```
* Install required pacakges through npm
* ```sh
  $ sudo npm install
  ```

* Get into the src directory and do
* ```sh 
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python syncdb`
  ```
* Load default test data
* ```sh
  $ python manage.py loaddata app/fixtures/*.json
  ```

* Make sure you reset the user table id sequence to be the latest in psql
* `SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));`

* Collect the static files into the correct staticfiles folder
* ```sh
  $ python manage.py collectstatic
  ```

* Start django server
* ```sh
  $ python manage.py runserver
  ```

9. Test api in your web browser by hitting
* `http://localhost:8000/api/v1/people/1/`


### Heroku deployment instruction

1. You need to merge all the code from master to branch environment-setup.
This is because: environment-setup branch has the database reference to the db in heroku. While on master, we only have db config referencing our local database. Also, environment-setup branch contains database migration files needed for creating proper migration scripts. Furthermore, heroku environment currently do not support SASS.

2. After the code is merged, you have to run this. This would compile all the .css.scss to .css.css files.
* ```sh
  $ sass --update ./app/static/stylesheets/
  ```
3. Go to ./smoothbenefits/settings.py, make sure you replace all .css.scss files to .css.css files. Make sure this is definitely done. Otherwise when deploying heroku, the automatically run  “python manage.py collectstatic” will fail

4. run “python manage.py makemigrations” to generate the migration files. Make sure you check these new migration files in. As you can see on this branch, the .gitignore file do not contain migration files like the .gitignore file on master do.

5. deploy to heroku from the “environment-setup” branch For example: “git push heroku environment-setup:master” if your remote heroku branch is called “heroku”

6. run “heroku run python manage.py migrate” to migrate the changes in model into database

7. run "heroku run python manage.py shell". In shell, run the following commands and confirm in the database usernames have been hashed.
*  ```sh 
   > from emailusernames.utils import migrate_usernames
   > migrate_usernames()
  '''
7. Then try to hit the heroku app. If it is not working, run “heroku logs” to see what is the logging on heroku say.

### Run unit tests
1. You can run unit tests by simply do 
* ```sh 
  $ python manage.py test
  ```
2. However, the above method is slow. You can leverage the pytest package to speed up your unit test run
3. To test with py.test, go to the project root and just do 
* ```sh 
  $ py.test app/
  ```
4. If the database was not created or you had new migration, please run your test with 
* ```sh 
  $ py.test --create-db app/
  ```
5. You can also run the tests on multiple threads to speed it up even more. Execute the following to do multi-thread testing
* ```sh
  $ py.test -n <num_of_threads> app/
  ```
6. Again, if the test db needs to be regenerated, you can do
* ```sh
  $ py.test -n <num_of_threads> --create-db app/
  ```
Make a change
