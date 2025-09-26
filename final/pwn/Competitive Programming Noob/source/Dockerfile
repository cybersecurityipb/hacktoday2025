FROM ubuntu:noble

EXPOSE 8000

RUN apt update
RUN apt-get install -y socat

RUN mkdir /pwn
WORKDIR /pwn

COPY flag.txt .
COPY beginner .
COPY ld-2.31.so .
COPY libc.so.6 .

RUN chmod -R 755 /pwn
RUN chmod 700 /usr/bin/* /bin/* /tmp /dev/shm
RUN chmod 755 /usr/bin/env /bin/dash /bin/bash /bin/sh /bin/cat /usr/bin/id /bin/ls

CMD socat TCP-LISTEN:8000,reuseaddr,fork EXEC:/pwn/beginner,su=nobody
