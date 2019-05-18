FROM python:3.7-alpine3.8

WORKDIR /app

COPY . /app

RUN pip3 install pipenv
RUN pipenv install

ENTRYPOINT [ "/usr/bin/python3" ]

CMD ["dnsupdate.py"]
