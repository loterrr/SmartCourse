FROM php:8.2-apache

# 1. Update apt and install Python 3
# (Cleaned up formatting to remove invisible characters)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql

# 2. Fix for "More than one MPM loaded" error
# We forcibly disable mpm_event and ensure mpm_prefork is active for PHP
RUN a2dismod mpm_event || true \
    && a2enmod mpm_prefork \
    && a2enmod rewrite

# 3. Copy source code
COPY . /var/www/html/

# 4. Set Permissions for Python
RUN chmod +x /var/www/html/backend/recommendation_algorithm.py

# 4.5 CRITICAL: Give Apache permission to write to files
# (Fixed the formatting issue here)
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# 5. Configure Port (Railway specific magic)
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

CMD ["apache2-foreground"]
