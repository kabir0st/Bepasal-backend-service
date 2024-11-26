FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt update && apt install -y libpq-dev libcairo2 gcc postgresql-client
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install watchdog
COPY . /app/
RUN chmod +x /app/src/entrypoint.sh

EXPOSE 8000
WORKDIR /app/src

RUN python manage.py collectstatic --noinput
ENTRYPOINT ["/app/src/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
