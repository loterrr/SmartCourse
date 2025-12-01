FROM php:8.2-apache

# --- THIS IS THE MISSING PART ---
# Install the PHP extensions for MySQL
RUN docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable mysqli
# --------------------------------

# Enable URL rewriting
RUN a2enmod rewrite

# Copy your source code
COPY . /var/www/html/

# Configure the port for Railway
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# Start Apache
CMD ["apache2-foreground"]
