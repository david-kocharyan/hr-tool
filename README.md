<div id="top"></div>
<h1 align="center">HR Tool Back End</h1>

![Build Status](https://img.shields.io/badge/Status-Development-green)
![Python](https://img.shields.io/badge/python-v3.8.10-blue)
![PostgreSQL](https://img.shields.io/badge/postgresql-12.9-blue)
![Django](https://img.shields.io/badge/Django-4.0.3-blue)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.13.1-blue)
![Simple JWT](https://img.shields.io/badge/Simple%20JWT-5.1.0-blue)

## About The Project

Human resources manager web tool.

### Built With

* [Python 3.8.10](https://www.python.org/)
* [PostgreSQL 12.9](https://www.postgresql.org/)
* [Django 4.0.1](https://www.djangoproject.com/)
* [Django RF 3.13.1](https://www.django-rest-framework.org/)
* [Simple JWT 5.1.0](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Getting Started

Here's how you can set up a project and what you need to do for it.

### Prerequisites

For running project, you should install on your machine`

* Python 3.8
* PostgreSQL 12.9

### Installation

Here's instruction for installing and setting up the app step by step._

1. Clone the repo`
   ```shell
   git clone 
   ```

2. Move to the working directory, install and activate your virtualenv`
   ```shell
    cd /project_path 
   ```
   ```shell
    python -m venv yourVenvName
   ```
   ```shell
    source yourVenvName/bin/activate
   ```

3. For PostgreSql adapter you should install on your machine (Linux/Ubuntu)`
   ```shell
    sudo apt-get update
    sudo apt-get install libpq-dev
   ```
   ```shell
    sudo apt-get install python-dev
    OR
    sudo apt-get install python3-dev
   ```

4. Install requirements`
   ```shell
    pip install -r requirements.txt
   ```

5. Set your .env file and migrate`
   ```shell
    python manage.py migration
   ```
6. Run`
   ```shell
    python manage.py runserver
   ```

<p align="center"><a href="#top">Back to top</a></p>