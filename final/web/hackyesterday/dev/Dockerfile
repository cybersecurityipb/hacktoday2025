# --- Build React Frontend ---
FROM node:14 AS react-build

WORKDIR /app

COPY ./frontend .

RUN npm install && \
	npm run build

# --- Final Setup with Nginx and FastAPI ---
FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y nginx supervisor chromium chromium-driver && \
	rm -rf /var/lib/apt/lists/*

COPY --from=react-build /app/build /usr/share/nginx/html
COPY api/ .

RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /var/uploads/pdf && \
    mkdir /var/uploads/images

COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
