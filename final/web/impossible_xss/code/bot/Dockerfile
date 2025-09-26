FROM node:20-bullseye-slim

WORKDIR /app

# system deps required by Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates fonts-liberation libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libx11-6 libxcomposite1 libxdamage1 libxrandr2 libxss1 libasound2 libglib2.0-0 chromium \
 && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json* ./
ENV PUPPETEER_SKIP_DOWNLOAD=true
RUN if [ -f package-lock.json ]; then npm ci --omit=dev --no-audit --no-fund; else npm install --omit=dev --no-audit --no-fund; fi

COPY . .

ENV NODE_ENV=production
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
EXPOSE 3001
CMD ["node", "app.js"]
