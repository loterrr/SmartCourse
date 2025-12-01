FROM php:8.2-apache

# Install PHP extensions AND Python
RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

RUN a2enmod rewrite
COPY . /var/www/html/
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf
CMD ["apache2-foreground"]
