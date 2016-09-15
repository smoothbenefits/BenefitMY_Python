BenefitMY_Python
================
### Setup your development environment
Please follow the following steps to start the app on your local machine

1. Setup the virtual environment. Make sure you downloaded and installed the virtual environment wrapper tool (https://virtualenvwrapper.readthedocs.org/en/latest/)
 ```sh
  $ mkvirtualenv benefitmy
  ```
* Make sure you have npm installed
 ```sh
  $ sudo apt-get install npm
  ```
* Install postgres (http://www.postgresql.org/download/macosx/) and then Create DB "Benefits_DB"
 ```sh
  $ createuser postgres
  $ createdb -O postgres -w Benefits_DB
  ```
* Pip install
 ```sh
  $ pip install -r requirements.txt
  ```
* Install required pacakges through npm
 ```sh
  $ sudo npm install
  ```
* Get into the src directory and do
 ```sh 
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python syncdb`
  ```
* Load default test data
 ```sh
  $ python manage.py loaddata app/fixtures/*.json
  ```
* Make sure you reset the user table id sequence to be the latest in psql
 ```sh SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));```
* Compile SASS and Collect the static files into the correct staticfiles folder
 ```sh
  $ gulp
  ```
* Start django server
 ```sh
  $ python manage.py runserver
  ```
* Test api in your web browser by hitting
 `http://localhost:8000/api/v1/people/1/`


### Run unit tests
1. You can run unit tests by simply do 
 ```sh 
  $ python manage.py test
  ```
* However, the above method is slow. You can leverage the pytest package to speed up your unit test run
* To test with py.test, go to the project root and just do 
 ```sh 
  $ py.test app/
  ```
* If the database was not created or you had new migration, please run your test with 
 ```sh 
  $ py.test --create-db app/
  ```
* You can also run the tests on multiple threads to speed it up even more. Execute the following to do multi-thread testing
 ```sh
  $ py.test -n <num_of_threads> app/
  ```
* Again, if the test db needs to be regenerated, you can do
 ```sh
  $ py.test -n <num_of_threads> --create-db app/
  ```
