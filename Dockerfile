FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

RUN a2enmod rewrite

# Kill extra MPMs at the source
RUN sed -i \
    -e 's/^LoadModule mpm_event_module/#LoadModule mpm_event_module/' \
    -e 's/^LoadModule mpm_worker_module/#LoadModule mpm_worker_module/' \
    /etc/apache2/mods-available/mpm_event.load \
    /etc/apache2/mods-available/mpm_worker.load || true

COPY . /var/www/html/

RUN chmod +x /var/www/html/backend/recommendation_algorithm.py && \
    chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

RUN sed -i 's/80/${PORT}/g' \
    /etc/apache2/sites-available/000-default.conf \
    /etc/apache2/ports.conf

CMD ["apache2-foreground"]
