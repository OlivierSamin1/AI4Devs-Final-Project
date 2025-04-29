FROM arm32v7/nginx:1.24-alpine

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Create directories for static files and media
RUN mkdir -p /app/static /app/media

# Create user for nginx
RUN adduser -D -H -u 1000 -s /bin/sh www-data

# Set proper permissions
RUN chown -R www-data:www-data /app /var/cache/nginx /var/log/nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && chown www-data:www-data /var/run/nginx.pid

# Switch to non-root user
USER www-data

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 