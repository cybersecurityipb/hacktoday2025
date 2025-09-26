# Dockerfile - PHP-FPM image for Laravel (PHP 8.3)
FROM php:8.3-fpm

# Install system deps and PHP extensions required by Laravel
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    git zip unzip libzip-dev libicu-dev libonig-dev libpng-dev libxml2-dev curl \
 && docker-php-ext-install pdo pdo_mysql mbstring intl xml zip bcmath \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy composer binary from official composer image
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Expose FPM port
EXPOSE 9000

# Default command
CMD ["php-fpm"]
