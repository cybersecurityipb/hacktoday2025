FROM openresty/openresty:alpine

COPY ./nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ./www /www
RUN echo "hacktoday{g4t3w4y_m1sc0nf1gur4t10n_c0z_tr0ubl3}" > /flag
RUN echo "passthepasswordisdontlookbehindpasswordsomethingiswatching" > /password

EXPOSE 80

CMD ["sh", "-c", "openresty -g 'daemon off;'"]