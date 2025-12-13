FROM php:8.2-apache

# System deps
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

# HARD FIX: only one Apache engine may exist
RUN apt-get purge -y apache2-mpm-event apache2-mpm-worker && \
    apt-get install -y apache2-mpm-prefork

RUN a2enmod rewrite

COPY . /var/www/html/

RUN chmod +x /var/www/html/backend/recommendation_algorithm.py

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

RUN sed -i 's/80/${PORT}/g' \
    /etc/apache2/sites-available/000-default.conf \
    /etc/apache2/ports.conf

CMD ["apache2-foreground"]
