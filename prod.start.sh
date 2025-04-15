#!/bin/sh

# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░ЗАПУСКАЕМ░ГУСЕЙ-РАЗВЕДЧИКОВ░░░░
# ░░░░░▄▀▀▀▄░░░▄▀▀▀▀▄░░░▄▀▀▀▄░░░░░
# ▄███▀░◐░░░▌░▐0░░░░0▌░▐░░░◐░▀███▄
# ░░░░▌░░░░░▐░▌░▐▀▀▌░▐░▌░░░░░▐░░░░
# ░░░░▐░░░░░▐░▌░▌▒▒▐░▐░▌░░░░░▌░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

python3 -m flask db init
python3 -m flask db migrate
python3 -m flask db upgrade

if [ "$APP_DEBUG" == "1" ]; then
        python3 app.py
else
        gunicorn -w 8 -b REDACTED wsgi:app
fi

exec "$@"