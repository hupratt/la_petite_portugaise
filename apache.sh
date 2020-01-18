#! /usr/bin/env bash

# Treat unset variables as an error when substituting
set -e

USE_STATIC_URL=${STATIC_URL:-'/static'}
USE_STATIC_PATH=${STATIC_PATH:-'/app/static'}
USE_DOC_ROOT=${DOC_ROOT:-'/var/www/html'}
USE_SERVER_NAME=${SERVER_NAME:-'example.com'}
USE_CERT_FILE=${CERT_FILE:-'/etc/pki/tls/certs/localhost.crt'}
USE_CERT_KEY_FILE=${CERT_KEY_FILE:-'/etc/pki/tls/private/localhost.key'}

if [ -f /etc/apache2/sites-available/example.conf ]; then
    content_server='<VirtualHost _default_:443>\n'
    content_server=$content_server'    DocumentRoot "${USE_DOC_ROOT};"\n'
    content_server=$content_server'    ServerName "${USE_SERVER_NAME};"\n'
    content_server=$content_server'    SSLCertificateFile "${USE_CERT_FILE};"\n'
    content_server=$content_server'    SSLCertificateKeyFile "${USE_CERT_KEY_FILE};"\n'
    content_server=$content_server'</VirtualHost>\n'
    # Overwrite config into target location
    printf "$content_server" > /etc/apache2/sites-available/example.conf
fi

exec "$@"
