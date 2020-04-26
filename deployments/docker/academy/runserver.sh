#!/usr/bin/env bash

HOST=$(echo "$1" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
PORT=$(echo "$2" | grep -oE "[0-9][0-9][0-9][0-9]")


if [[ "$HOST" && "$PORT" ]]; then
  python manage.py makemigrations || echo "No changes detected!!"
  python manage.py migrate
  python manage.py runserver "$HOST:$PORT" --insecure
else
  echo "Error: Make sure you are followin example <sh $0 0.0.0.0 5000>"
fi
