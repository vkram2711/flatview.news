#!/bin/bash
set -e

# Render.com provides PORT env var; default to 10000
export PORT=${PORT:-10000}

# Generate nginx config from template, substituting only ${PORT}
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Remove default nginx site if present
rm -f /etc/nginx/sites-enabled/default

exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
