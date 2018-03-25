FROM nginx
MAINTAINER Calum Boal - "cgboal@protonmail.com"

RUN apk --no-cache add procps util-linux pciutils usbutils coreutils binutils findutils grep

COPY start.sh /
COPY nginx.conf /etc/nginx/
COPY nginx-secure.conf /etc/nginx/

COPY dhparams.pem /etc/ssl/private/
CMD /start.sh
