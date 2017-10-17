FROM frolvlad/alpine-python3

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["Python", "dnsupdate.py"]