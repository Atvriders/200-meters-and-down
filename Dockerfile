FROM nginx:alpine

COPY build/index.html /usr/share/nginx/html/index.html
COPY build/200-meters-and-down.txt build/200-meters-and-down.pdf /usr/share/nginx/html/
COPY chapters/ /usr/share/nginx/html/chapters/
COPY audiobook/ /usr/share/nginx/html/audiobook/
COPY docker/audiobook-index.html /usr/share/nginx/html/audiobook/index.html
