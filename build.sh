#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
# Render's free web services do not support a pre-deploy command.
# For this Blueprint, migrations are applied during the build before the new
# instance starts. For a paid service, move this command to preDeployCommand.
python manage.py migrate --noinput
