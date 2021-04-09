FROM python:3.9 as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

RUN python3 manage.py collectstatic --no-input
EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "dj_project.asgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install debugpy
ENV DEBUG_IN_CONTAINER 1

WORKDIR /app
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver 0.0.0.0:8000

# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess manage.py runserver 0.0.0.0:8000

###########START NEW IMAGE: PRODUCTION ###################
FROM base as dev

# CMD flask run -h 0.0.0 -p 5000
CMD python manage.py runserver 0.0.0.0:8000