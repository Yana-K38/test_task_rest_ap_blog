FROM blog_api:latest AS app

FROM nginx:1.21-alpine

RUN rm -rf /etc/nginx/conf.d
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=app /app/static /var/html/static