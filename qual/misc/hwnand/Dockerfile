FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y socat

RUN pip install z3-solver

COPY chall.py /app/chall.py

RUN echo 'flag = "hacktoday{0a19709aa4d1ab65}"' > flag.py

EXPOSE 80

CMD ["sh", "-c", "socat TCP-LISTEN:80,reuseaddr,fork EXEC:'python chall.py'"]