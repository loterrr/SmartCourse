FROM php:8.2-apache

# 1. Update apt and install Python 3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

# 2. Enable Rewrite
RUN a2enmod rewrite

# 3. Copy source code
COPY . /var/www/html/

# 4. Set Permissions for Python
RUN chmod +x /var/www/html/backend/recommendation_algorithm.py

# 5. CRITICAL: Give Apache permission to write to files
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# 6. Configure Port
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# 7. RUNTIME CMD (The Fix)
# This runs every time the server starts. It forces mpm_event OFF and mpm_prefork ON.
CMD ["/bin/sh", "-c", "a2dismod mpm_event mpm_worker && a2enmod mpm_prefork && apache2-foreground"]
