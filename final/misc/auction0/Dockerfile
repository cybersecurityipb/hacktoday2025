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
    && rm -rf /tmp/contracts/lib \
    # Download OZ v5.0.0 tarball (no git) and place at /tmp/lib/openzeppelin-contracts
    && mkdir -p /tmp/lib \
    && wget -qO /tmp/oz.tar.gz https://github.com/OpenZeppelin/openzeppelin-contracts/archive/refs/tags/v5.0.0.tar.gz \
    && tar -xzf /tmp/oz.tar.gz -C /tmp/lib \
    && mv /tmp/lib/openzeppelin-contracts-5.0.0 /tmp/lib/openzeppelin-contracts \
    && rm /tmp/oz.tar.gz \
    && forge build \
    && rm -rf /tmp/contracts \
    && true