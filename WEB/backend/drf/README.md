# DRF Authentication

Cloned from https://github.com/studygyaan/django-rest-framework-tutorial

# References

https://github.com/James1345/django-rest-knox

# Requirements

* Python 3.8.x
* pip3 (sudo apt install python3-pip)
* python3.8-venv (sudo apt install python3.8-venv)


# Installation

* cd ~{project dir}/WEB/backend
* python3 -m venv django-venv
* source ./django-venv/bin/activate
#
* cp secrets.example.json secrets.json
* edit secrets.json with your own credentials
#
* cd ~{project dir}/WEB/backend/drf
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* python manage.py createsuperuser
* python manage.py runserver