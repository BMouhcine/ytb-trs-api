FROM python:3.9.1

#RUN apt-get update -y && apt-get install -y python3.8 python-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt && pip install -U pyopenssl
COPY . /app

EXPOSE 5000

CMD [ "python", "./yta.py" ]
