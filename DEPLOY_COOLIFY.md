# Guia de Deploy no Coolify

Este guia descreve o passo a passo para colocar sua aplicação Django no ar usando sua VPS com Coolify.

## 1. Preparação do Repositório

Certifique-se de que todas as alterações recentes (Dockerfile, entrypoint.sh, settings.py, etc.) foram enviadas para o seu repositório remoto (GitHub, GitLab, etc.).

```bash
git add .
git commit -m "Configuração para deploy no Coolify"
git push origin main
```

## 2. Criar Banco de Dados (Recomendado)

No painel do Coolify:
1. Vá para o seu projeto (ou crie um novo).
2. Clique em **+ New Resource**.
3. Selecione **Database** > **PostgreSQL**.
4. Siga os passos para criar.
5. Após criado, entre nas configurações do banco e copie a **Internal Connection URL** (algo como `postgresql://postgres:password@ip:5432/postgres`). Você vai precisar dela.

## 3. Configurar a Aplicação

1. Volte ao seu projeto no Coolify.
2. Clique em **+ New Resource**.
3. Selecione **Git Repository** (ou "Public Repository" se for público).
4. Conecte seu repositório e selecione a branch `main`.
5. **Build Pack**: O Coolify deve detectar o `Dockerfile`. Se perguntar, confirme que quer usar **Dockerfile**.
6. **Port**: Defina a porta como `8000`.

## 4. Variáveis de Ambiente

Antes de fazer o deploy, vá na aba **Environment Variables** da sua aplicação e adicione:

| Chave | Valor (Exemplo) | Descrição |
|-------|-----------------|-----------|
| `SECRET_KEY` | `sua-chave-secreta-longa-e-aleatoria` | Gere uma nova chave segura. |
| `DEBUG` | `False` | Desativa o modo debug para segurança. |
| `ALLOWED_HOSTS` | `carros.dominio.qzz.io` | Seu domínio de produção. |
| `CSRF_TRUSTED_ORIGINS` | `https://carros.dominio.qzz.io` | Necessário para formulários (POST) funcionarem via HTTPS. |
| `GEMINI_API_KEY` | `AIza...` | Sua chave da API do Google Gemini. |
| `DATABASE_URL` | `postgresql://...` | A URL interna do banco que você copiou no passo 2. |

> **Nota**: Se você não configurar `DATABASE_URL`, a aplicação usará SQLite. Isso funciona, mas os dados podem ser perdidos se o volume não for configurado corretamente. O PostgreSQL é muito mais seguro para produção.

## 5. Configuração de Domínio no Coolify

1. Vá nas configurações da sua aplicação no Coolify.
2. Em **Domains**, adicione: `https://carros.dominio.qzz.io`.
   - O Coolify deve configurar automaticamente o certificado SSL (HTTPS).
3. (Opcional) Se você quiser que a URL base redirecione para `/cars`, você precisará configurar isso no seu código (views) ou usar um proxy reverso customizado, mas acessar `https://carros.dominio.qzz.io/cars` funcionará nativamente.

Se sua aplicação faz upload de imagens (pasta `media`), você precisa persistir esse diretório.
1. Vá na aba **Storage** (ou Volumes).
2. Adicione um volume:
   - **Source Path**: (Deixe o Coolify gerenciar ou defina um caminho no host)
   - **Destination Path**: `/app/media`

## 6. Deploy

1. Clique no botão **Deploy** no canto superior direito.
2. Acompanhe os logs de "Build" e "Deploy".
3. O script `entrypoint.sh` que criamos vai rodar automaticamente as migrações e coletar os arquivos estáticos.

## 7. Acessar

Após o deploy finalizar com sucesso:
1. O Coolify deve gerar um domínio automático (ex: `http://random-name.seu-coolify.com`) ou você pode configurar o seu em **Domains**.
2. Acesse e teste a aplicação!
