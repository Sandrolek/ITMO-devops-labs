FROM nginx:1.27.1-alpine

COPY html /etc/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.crt /etc/nginx/ssl/nginx.crt
COPY nginx.key /etc/nginx/ssl/nginx.key

CMD ["nginx"]