# Deployment

Production runs on one AWS EC2 instance (t3.micro, Elastic IP `40.177.208.177`)
as three containers: **Caddy** (HTTPS + `/media/`), **web** (Django + gunicorn +
whitenoise) and **Postgres 16**.

```
push to fix-storages-import
  -> CI (checks, migrations, tests, image build)
  -> build linux/amd64 image, push to ghcr.io/<owner>/<repo>/web:<sha>
  -> scp infra/ to /opt/fgen, back up Postgres, docker compose pull + up
  -> wait for /healthz/, then smoke-test https://fgen.ca
```

## GitHub secrets

| Secret | Value |
|---|---|
| `EC2_HOST` | `40.177.208.177` |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | the full private key (PEM, including BEGIN/END lines) |
| `ADMIN_PASSWORD` | optional: Django admin password, re-applied on every deploy |
| `ADMIN_USERNAME` | optional, defaults to `admin` |
| `EMAIL_HOST_PASSWORD` | Office365 password for info@fgen.ca |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key (`pk_...`) |
| `STRIPE_SECRET_KEY` | Stripe secret key (`sk_...`) |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (`whsec_...`) for `https://www.fgen.ca/stripe_webhook` |

The app secrets are written into `/opt/fgen/.env` on every deploy. `DJANGO_SECRET_KEY`
and `POSTGRES_PASSWORD` are generated once on the host and never leave it.

## Host layout (`/opt/fgen`)

| Path | What |
|---|---|
| `.env` | all runtime config and secrets (template: `infra/.env.example`); never in git |
| `docker-compose.prod.yml`, `caddy/Caddyfile` | copied from `infra/` on every deploy |
| `backups/pre-deploy-*.sql` | Postgres dump taken before each deploy (last 10 kept) |

Data lives in Docker volumes and survives every deploy:
`fgen_pg_data` (database), `fgen_media` (uploads), `fgen_caddy_data` (certificates).
Never run `docker compose down -v`.

## Everyday commands (on the host)

```bash
cd /opt/fgen
C="docker compose --env-file .env -f docker-compose.prod.yml"
$C ps                                   # status
$C logs -f web                          # app logs
$C exec web python manage.py createsuperuser
$C exec web python manage.py changepassword admin
```

## Rollback

- **Code:** set `IMAGE_TAG=<older sha>` in `.env`, then `$C up -d web`.
- **Database:** `$C exec -T postgres psql -U fgen -d fgen < backups/pre-deploy-<timestamp>.sql`

## Local development

```bash
python -m venv venv && venv/Scripts/activate   # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
