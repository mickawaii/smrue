# smrue

### Pip
`pip freeze > requirements.txt`
`pip install -r requirements.txt`

### Heroku
###### Restart heroku
`heroku restart`

###### Scale dinos
`heroku ps:scale web=1`

###### Check state
`heroku ps`

###### See logs
`heroku logs -t -a smrue-mi`

###### Django-shell
`heroku run python manage.py shell`

###### Run migrations
`heroku run python manage.py migrate`
