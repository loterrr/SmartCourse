FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

RUN a2enmod rewrite

# CRITICAL: fix MPM conflict
RUN a2dismod mpm_event mpm_worker || true \
    && a2enmod mpm_prefork

COPY . /var/www/html/

RUN chmod +x /var/www/html/backend/recommendation_algorithm.py

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

RUN sed -i 's/80/${PORT}/g' \
    /etc/apache2/sites-available/000-default.conf \
    /etc/apache2/ports.conf

CMD ["apache2-foreground"]
