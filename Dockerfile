FROM php:8.2-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

# Enable rewrite
RUN a2enmod rewrite

# ✅ Correct Apache MPM configuration (THIS is the fix)
RUN a2dismod mpm_event mpm_worker && \
    a2enmod mpm_prefork

# Copy app
COPY . /var/www/html/

# Permissions
RUN chmod +x /var/www/html/backend/recommendation_algorithm.py && \
    chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Railway port fix
RUN sed -i 's/80/${PORT}/g' \
    /etc/apache2/sites-available/000-default.conf \
    /etc/apache2/ports.conf

CMD ["apache2-foreground"]
