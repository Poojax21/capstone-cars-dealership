FROM python:3.11-slim

WORKDIR /app

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY server/ ./

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py seed && gunicorn djangoproj.wsgi:application --bind 0.0.0.0:8000"]
