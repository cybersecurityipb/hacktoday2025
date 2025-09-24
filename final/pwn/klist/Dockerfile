FROM ubuntu:25.04

RUN apt-get update
RUN apt-get install -y qemu-system-x86 socat

COPY run.sh /run.sh
COPY artifacts/ /artifacts/
COPY flag.txt /flag.txt

CMD ["socat", "TCP-LISTEN:1337,fork,reuseaddr", "EXEC:/run.sh"]