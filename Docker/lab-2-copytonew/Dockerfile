FROM ubuntu:22.04

# Install nginx and clean up apt cache in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/www/html/*

# Copy website
COPY index.html /var/www/html/index.nginx-debian.html

# Expose HTTP port
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]