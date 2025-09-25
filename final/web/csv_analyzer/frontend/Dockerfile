FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/custom.conf
COPY index.html /usr/share/nginx/html/index.html