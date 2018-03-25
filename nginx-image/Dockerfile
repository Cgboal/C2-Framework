FROM nginx
MAINTAINER Calum Boal - "cgboal@protonmail.com"

RUN apt-get update && apt-get install -y procps grep gawk

COPY start.sh /
COPY nginx.conf /etc/nginx/
COPY nginx-secure.conf /etc/nginx/

COPY dhparams.pem /etc/ssl/private/
CMD /start.sh
