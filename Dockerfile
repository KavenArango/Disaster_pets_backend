FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_APP=./app.py

ENV FLASK_RUN_HOST=0.0.0.0

RUN apk -U add alpine-sdk gcc musl-dev unixodbc-dev libffi-dev
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.6.1.1-1_amd64.apk && curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.6.1.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.6.1.1-1_amd64.apk && apk add --allow-untrusted mssql-tools_17.6.1.1-1_amd64.apk


#linux-headers
#python3-dev
#openssl-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . /code

CMD ["flask", "run"]
