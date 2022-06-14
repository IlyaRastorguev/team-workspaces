FROM python:3.9

COPY . /app
COPY pip.conf /etc/pip.conf

RUN pip install -r /app/requirements.txt

CMD python3 manage.py runserver 0.0.0.0:8000
