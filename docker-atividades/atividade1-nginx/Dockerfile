FROM nginx:alpine
LABEL maintainer="cristiano.1973.on@gmail.com"
LABEL description="Servidor Web NGINX - SENAI Redes"
LABEL version="1.0"

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY ./site/ .

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]