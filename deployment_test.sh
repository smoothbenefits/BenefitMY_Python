# deploy to staging or test environment
#!/bin/sh -e
APP_NAME=$1
DB_NAME=$2

# dump the heroku remote if it exists already
test `git remote | grep heroku` && git remote rm heroku

git remote add heroku git@heroku.com:$APP_NAME.git
git fetch origin --unshallow
git fetch heroku --unshallow
MIGRATION_CHANGES=$(git diff HEAD heroku/master --name-only -- db | wc -l)
echo "$MIGRATION_CHANGES db changes."

PREV_WORKERS=$(heroku ps --app $APP_NAME | grep "^worker." | wc -l | tr -d ' ')

# migrations require downtime so enter maintenance mode
if test $MIGRATION_CHANGES -gt 0; then
  heroku maintenance:on --app $APP_NAME

  # Make sure workers are not running during a migration
  heroku scale worker=0 --app $APP_NAME
fi

# deploy code changes (and implicitly restart the app and any running workers)
git push heroku $CIRCLE_SHA1:master

# deploy the correct setting file
heroku config:set DJANGO_SETTINGS_MODULE=Smoothbenefits.$APP_NAME-settings --app $APP_NAME

# reset database to clean up all existing data
heroku pg:reset $DB_NAME --app $APP_NAME --confirm $APP_NAME

# run database migrations to restore lastest database schema
heroku run python manage.py migrate --app $APP_NAME

# load predefine data in fixtures
heroku run python manage.py loaddata app/fixtures/*.json --app $APP_NAME

# update data with mirgration script for database
sh ./data_migration.sh ./data_migration

# Generate the stylesheet and collect static
heroku run gulp

# reapply worker
heroku scale worker=$PREV_WORKERS --app $APP_NAME

# force restart app to make new setting file take effects
heroku restart --app $APP_NAME

heroku maintenance:off --app $APP_NAME
