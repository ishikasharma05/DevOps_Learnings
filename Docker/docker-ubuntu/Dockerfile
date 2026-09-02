FROM ubuntu:latest

RUN apt update -y
RUN apt install -y nginx

RUN rm -rf /var/www/html/*

COPY index.html /var/www/html/index.nginx-debian.html

EXPOSE 80

CMD ["nginx","-g","daemon off;"]
