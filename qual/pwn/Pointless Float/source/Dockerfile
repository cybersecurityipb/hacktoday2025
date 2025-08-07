FROM ubuntu:noble as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

WORKDIR /srv/app
COPY flag.txt flag.txt
COPY chall run
COPY libc.so.6 libc.so.6
COPY ld-linux-x86-64.so.2 ld-linux-x86-64.so.2
