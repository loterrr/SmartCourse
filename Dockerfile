FROM php:8.2-apache

# ---- CACHE BUSTER (Method 1) ----
# Change this number to force a fresh build on Railway
ARG CACHE_BUST=1

# System dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

# Enable Apache rewrite
RUN a2enmod rewrite

# FIX Apache MPM: only prefork is allowed with mod_php
RUN a2dismod mpm_event mpm_worker && \
    a2enmod mpm_prefork

# Copy application code
COPY . /var/www/html/

# Permissions
RUN chmod +x /var/www/html/backend/recommendation_algorithm.py && \
    chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Railway dynamic port support
RUN sed -i 's/80/${PORT}/g' \
    /etc/apache2/sites-available/000-default.conf \
    /etc/apache2/ports.conf

# Start Apache
CMD ["apache2-foreground"]
