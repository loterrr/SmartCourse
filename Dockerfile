FROM php:8.2-apache

# Copy your source code into the web server directory
COPY . /var/www/html/

# Enable URL rewriting (useful for routing)
RUN a2enmod rewrite

# Allow the web server to bind to Railway's dynamic port
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# Start Apache
CMD ["apache2-foreground"]
