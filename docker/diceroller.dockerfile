FROM ubuntu:22.04

EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=password

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --upgrade "pip>=24.0" \
    && pip3 install django==5.2.5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./diceroller ./diceroller

RUN pip3 install ./diceroller && \
    python3 -c "import diceroller; print('diceroller install successful')" && \
    rm -rf ./diceroller

COPY ./site ./site

RUN python3 ./site/project/manage.py migrate && \
    python3 ./site/project/manage.py createsuperuser --noinput

CMD ["python3","./site/project/manage.py","runserver", "0.0.0.0:8000"]