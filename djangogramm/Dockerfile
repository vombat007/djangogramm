FROM python:3.11.1


SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs


Run apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash djangogramm && chmod 777 /opt /run

WORKDIR /djangogramm

RUN mkdir /djangogramm/static && mkdir /djangogramm/media && chown -R djangogramm:djangogramm /djangogramm && chmod 755 /djangogramm
# copy project
COPY --chown=djangogramm:djangogramm . .

RUN pip install -r requirements.txt

USER djangogramm

CMD ["waitress-serve", "--port=8000", "djangogramm.wsgi:application"]