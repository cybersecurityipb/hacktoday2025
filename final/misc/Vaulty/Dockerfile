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
    && true
    && tr -d '\r' < /entrypoint.sh > /entrypoint.sh