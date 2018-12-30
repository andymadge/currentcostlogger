FROM python:3.7-alpine3.8

RUN pip install pyserial

WORKDIR /root

COPY ./currentcost.py .

CMD ["./currentcost.py"]