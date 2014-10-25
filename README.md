BenefitMY_Python
================

Please follow the following steps to start the app on your local machine

1. install django
`pip install django`
`pip install djangorestframework`

2. install postgres

3. create DB "Benefits_DB"
`user: "postgres"`
`password: ""`

4. get into the src directory
`python manage.py makemigrations app`
`python manage.py migrate`
`python syncdb`

5. load default test data
`python manage.py loaddata app/fixtures/*.json`

6. Make sure you reset the user table id sequence to be the latest in psql
`SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));`

7. Collect the static files into the correct staticfiles folder
`python manage.py collectstatic`

8. start django server
`python manage.py runserver`

9. test api in your web browser by
`http://localhost:8000/api/v1/people/1/`
