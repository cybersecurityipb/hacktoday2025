FROM dimasmaualana/eth:latest

COPY deploy/ /home/ctf/
COPY contracts /tmp/contracts

RUN true \
    && cd /home/ctf \
    && pip install -r requirements.txt --break-system-packages \
    && cd /tmp \
    && printf "[profile.default]\nsrc = 'contracts'\nout = '/home/ctf/compiled'\nremappings = ['lib/=lib/']\n" > foundry.toml \
    && apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && rm -rf /var/lib/apt/lists/* \
    # Remove any partial vendored libs under contracts/ so they don't get compiled
    && forge build \
    && rm -rf /tmp/contracts \
    && tr -d '\r' < /entrypoint.sh > /entrypoint2.sh \
    && cp /entrypoint2.sh  /entrypoint.sh \
    && tr -d '\r' < /startup/96-start-launcher > /startup/96-start-launcher2 \
    && cp /startup/96-start-launcher2  /startup/96-start-launcher \
    && rm /startup/96-start-launcher2
    && true