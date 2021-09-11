FROM nginx:1.15
LABEL MAINTAINER="Hamed mohammadi | https://.com | mohammadih87@yahoo.com"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]