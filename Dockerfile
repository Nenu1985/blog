FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y
RUN pip install --upgrade pip

RUN groupadd -r admin && useradd -r -g admin admin

RUN mkdir -p /app/media /app/static /app/static_root\
  && chown -R admin:admin /app/

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}
RUN SECRET_KEY=dummy STATIC_URL=${STATIC_URL} python3 manage.py collectstatic --no-input

EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "dj_project.asgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]