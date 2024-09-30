### Linting Tool
install flake8 package

<code>
docker-compose run --rm app sh -c "flake8"
</code>


## Testing
<code>
docker-compose run --rm app sh -c "python manage.py test"
</code>