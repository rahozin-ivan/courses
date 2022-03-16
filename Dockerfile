FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init --create-home -r -u 1000 -g ${APP_USER} ${APP_USER}

ARG APP_DIR=/home/${APP_USER}/project/
RUN mkdir ${APP_DIR} && chown ${APP_USER}:${APP_USER} ${APP_DIR}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    wget \
    binutils \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_DIR}

COPY requirements.txt ${APP_DIR}
RUN pip install -r requirements.txt

COPY --chown=${APP_USER}:${APP_USER} . ${APP_DIR}

USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "conf.wsgi"]
