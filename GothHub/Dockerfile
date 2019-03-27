FROM python:3.7.2-alpine
ENV PYTHONUNBUFFERED 1

# Creating working directory
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code

# Copying requirements
ADD . /code
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]