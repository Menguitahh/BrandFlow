web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn BrandFlow.wsgi:application --bind 0.0.0.0:$PORT

