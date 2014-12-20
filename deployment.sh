# deployment script
#!/bin/sh -e
APP_NAME=$1

# dump the heroku remote if it exists already
test `git remote | grep heroku` && git remote rm heroku

git remote add heroku git@heroku.com:$APP_NAME.git
git fetch heroku
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

# run database migrations if needed and restart background workers once finished
if test $MIGRATION_CHANGES -gt 0; then
  heroku run python manage.py makemigrations --app $APP_NAME
  heroku run python manage.py migrate --app $APP_NAME
  heroku scale worker=$PREV_WORKERS --app $APP_NAME
  heroku restart --app $APP_NAME
fi

heroku maintenance:off --app $APP_NAME
