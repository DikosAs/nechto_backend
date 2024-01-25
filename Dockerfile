FROM python:3.11.3

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/


COPY . /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5338

CMD ["python3", "manage.py runserver 0.0.0.0:5338"]
