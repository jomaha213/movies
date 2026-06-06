#!/usr/bin/env bash
export PATH="/opt/render/python/3.12/bin:$PATH"
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python create_superuser.py