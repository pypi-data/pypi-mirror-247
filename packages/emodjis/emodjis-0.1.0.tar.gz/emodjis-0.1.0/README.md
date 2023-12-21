# emodjis


## Install

pip install emodjis

## Configuration

Add 

> ["rest_framework",
"django_filters",
"drf_spectacular",
"corsheaders",
"emodjis",]

to INSTALLED_APPS in your django settings.

Set SPECTACULAR_SETTINGS and REST_FRAMEWORK in your settings.

set a .env file with the following values:

> SERVER_URL=http://127.0.0.1:8000

> CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000

> DB_ENGINE=

> DB_HOST=

> DB_USER=

> DB_PASSWORD=

> DB_PORT=
