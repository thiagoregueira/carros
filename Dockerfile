# Usar imagem base leve do Python
FROM python:3.13-slim

# Variáveis de ambiente para otimização e logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema mínimas necessárias
# gcc e libpq-dev são comuns para compilar pacotes python se necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Copiar script de entrypoint e dar permissão de execução
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Criar usuário não-root para segurança
RUN useradd -m appuser

# Criar diretório de mídia e ajustar permissões
RUN mkdir -p /app/media && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app/media

# Mudar para o usuário não-root
USER appuser

# Expor a porta da aplicação
EXPOSE 8000

# Definir entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Comando de inicialização usando Gunicorn (servidor de produção)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
