#!/bin/sh

# Sair imediatamente se um comando falhar
set -e

# Rodar migrações do banco de dados
echo "Rodando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar o servidor
echo "Iniciando servidor..."
exec "$@"
