FROM python:3.9-alpine3.13

LABEL maintainer="navarajpokharel@outlook.com"

ENV DockerHOME=/home/app/webapp \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Create directory for the app user
RUN mkdir -p $DockerHOME \
    && addgroup -S app && adduser -S app -G app \
    && chown app:app $DockerHOME

# Switch to the app user
USER app

WORKDIR $DockerHOME

# Upgrade pip and install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . $DockerHOME

ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
