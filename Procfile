web: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin_if_missing && gunicorn BrandFlow.wsgi:application --bind 0.0.0.0:$PORT

