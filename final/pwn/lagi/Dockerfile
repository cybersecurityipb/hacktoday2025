FROM ubuntu:25.04

WORKDIR /app/

RUN apt-get update && \
	apt-get install socat -y

COPY ./chall /app/run
COPY ./flag.txt /app/flag.txt

RUN groupadd --system ctf && \
	useradd -M -d /app -g ctf player && \
	chmod +r /app/flag.txt && \
	chmod +x /app/run

USER player

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'/app/run',stderr"]