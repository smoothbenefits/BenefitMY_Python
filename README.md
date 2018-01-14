BenefitMY_Python
================
### Setup your development environment
Please follow the following steps to start the app on your local machine

1. Setup the virtual environment. Make sure you downloaded and installed the virtual environment wrapper tool (https://virtualenvwrapper.readthedocs.org/en/latest/)
 
          $ mkvirtualenv benefitmy

2. Make sure you have npm installed
 
          $ sudo apt-get install npm

3. Install postgres (http://www.postgresql.org/download/macosx/) and then Create DB "Benefits_DB"
 
          $ createuser postgres
          $ createdb -O postgres -w Benefits_DB

4. Pip install
         
          $ pip install -r requirements.txt
 
5. Install required pacakges through npm
 
           $ sudo npm install

6. Get into the src directory and do
 
           $ python manage.py makemigrations
           $ python manage.py migrate
           $ python syncdb

7. Load default test data

         $ python manage.py loaddata app/fixtures/*.json

8. Make sure you reset the user table id sequence to be the latest in psql
 
         SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));

9. Compile SASS and Collect the static files into the correct staticfiles folder

        $ gulp

10. Start django server

        $ python manage.py runserver

11. Test api in your web browser by hitting
 
         http://localhost:8000/api/v1/people/1/


### Run unit tests
1. You can run unit tests by simply do 

           $ python manage.py test

2. However, the above method is slow. You can leverage the pytest package to speed up your unit test run

3. To test with py.test, go to the project root and just do 

           $ py.test app/

4. If the database was not created or you had new migration, please run your test with 

          $ py.test --create-db app/


5. You can also run the tests on multiple threads to speed it up even more. Execute the following to do multi-thread testing

          $ py.test -n <num_of_threads> app/


6. Again, if the test db needs to be regenerated, you can do

          $ py.test -n <num_of_threads> --create-db app/
