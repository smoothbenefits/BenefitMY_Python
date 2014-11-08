BenefitMY_Python
================

Please follow the following steps to start the app on your local machine

0. Install coffeescript component. This is for the coffee javascript files
`sudo npm install -g coffee-script`

1. Install django
`sudo apt-get install python-psycopg2`
`pip install django`
`pip install djangorestframework`
 pip install django-pipeline
 pip install django-email-as-username


2. Install postgres

3. Create DB "Benefits_DB"
`user: "postgres"`
`password: ""`

4. Get into the src directory
`python manage.py makemigrations`
`python manage.py migrate`
`python syncdb`

5. Load default test data
`python manage.py loaddata app/fixtures/*.json`

6. Make sure you reset the user table id sequence to be the latest in psql
`SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));`

7. Collect the static files into the correct staticfiles folder
`python manage.py collectstatic`

8. Start django server
`python manage.py runserver`

9. Test api in your web browser by
`http://localhost:8000/api/v1/people/1/`

10. After each update, run through the following commands:
`pip install -r
