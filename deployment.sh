# deployment script
#!/bin/sh -e
APP_NAME=$1
DB_NAME=$2

case $APP_NAME in
	# Order is important here
	*"staging"*)
		sh ./deployment_test.sh $APP_NAME $DB_NAME
		;;
	*"demo"*)
		sh ./deployment_beta.sh $APP_NAME $DB_NAME
		;;
	*"beta"*)
		sh ./deployment_beta.sh $APP_NAME $DB_NAME
		;;
	*"prod"*)
		sh ./deployment_prod.sh $APP_NAME $DB_NAME # have not created yet
		;;
esac
