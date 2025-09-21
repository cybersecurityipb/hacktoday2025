FROM ubuntu:noble as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

WORKDIR /srv/app
COPY flag.txt flag.txt
COPY beginner run
COPY libc.so.6 libc.so.6
COPY ld-2.31.so ld-2.31.so
