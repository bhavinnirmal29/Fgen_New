# FGEN Website — Deployment Guide

This is the single source of truth for shipping changes: local setup, GitHub, and Heroku.
It supersedes `Deploy_Steps.txt` (kept for history) and folds in the old Cloudinary-only guide.

## 0. One-time setup: environment variables

As of this update, `Fgen_New/settings.py` no longer hardcodes secrets — it reads them from
environment variables (with safe, non-secret local defaults where possible). This was necessary
because the previous file had a live database password, email password, and API keys committed
in plaintext to git history.

**Locally:**
1. Copy `.env.example` to `.env` (this file is gitignored, never commit it).
2. Fill in real values only for the features you're testing locally (e.g. leave Stripe/email
   blank if you're not testing payments/email — the app degrades gracefully).

**On Heroku**, set the same variables as config vars (see step 4 below).

### ⚠️ Rotate these credentials

The following were committed in plaintext in git history on the `origin` GitHub remote and
should be treated as compromised — rotate them even though they're no longer in the code:
- The Office 365 email app password for `info@fgen.ca`
- The Postgres database password (rotate via Heroku Postgres credentials rotation, or provision
  a new database)
- Cloudinary API secret
- Django `SECRET_KEY` (generate a fresh one for production)

Stripe keys in the old file were **test-mode** keys (`sk_test_...`/`pk_test_...`), so the blast
radius there is low, but rotate them too if you want to be thorough.

---

## 1. Local verification checklist

Before pushing anything, run through this locally:

```bash
# from the project root, with your venv/interpreter active
pip install -r requirements.txt
python manage.py makemigrations --check   # should say "No changes detected"
python manage.py migrate
python manage.py check
python manage.py runserver
```

Then in the browser, click through:
- `/` — Home (Vision & Mission and Testimonials titles are now black/bold)
- `/about/` — About Us (new **Executives** section below Leadership Team; no more `+` signs in
  the impact numbers)
- `/programs/` — Programs (title reads "FGEN Neuroscience Presentations"; booking form shows once
  added in admin)
- `/involved/` — Get Involved (new **FGEN EXECUTIVE APPLICATIONS** section below Partnerships)
- `/contact_us/` — submit the form; it should redirect to a success page even if email delivery
  fails (check the terminal log for a caught exception, not a 500 page)

---

## 2. Push to GitHub

```bash
git status                     # review what's staged
git add <files>                # add specific files, not -A, to avoid staging secrets by accident
git commit -m "Describe the change"
git push origin fix-storages-import   # or your working branch
```

Then open a PR into `master` on GitHub (`bhavinnirmal29/Fgen_New`) and merge once reviewed.

**Before merging to `master`**, double check `git diff` doesn't include:
- Anything in `.env`
- `db.sqlite3` (already gitignored, but was tracked historically — see note at the bottom)

---

## 3. Deploy to Heroku

Heroku pulls from its own git remote (`heroku`, not `origin`). Two ways to deploy:

**Option A — push directly:**
```bash
git push heroku master
```

**Option B — connect GitHub auto-deploy** (recommended going forward): in the Heroku dashboard,
under your app → Deploy tab → GitHub → enable automatic deploys from `master`, so every merged
PR ships automatically.

### 4. Set Heroku config vars (one-time, or whenever a secret rotates)

```bash
heroku login                 # opens a browser; do this once per machine
heroku config:set DJANGO_SECRET_KEY="<generate with: python -c 'import secrets; print(secrets.token_urlsafe(50))'>" --app fgen
heroku config:set DJANGO_DEBUG=False --app fgen

heroku config:set EMAIL_HOST=smtp.office365.com --app fgen
heroku config:set EMAIL_HOST_USER=info@fgen.ca --app fgen
heroku config:set EMAIL_HOST_PASSWORD="<new rotated app password>" --app fgen
heroku config:set DEFAULT_FROM_EMAIL=info@fgen.ca --app fgen

heroku config:set CLOUDINARY_CLOUD_NAME="<value>" --app fgen
heroku config:set CLOUDINARY_API_KEY="<value>" --app fgen
heroku config:set CLOUDINARY_API_SECRET="<new rotated secret>" --app fgen

heroku config:set STRIPE_PUBLIC_KEY_TEST="<value>" --app fgen
heroku config:set STRIPE_SECRET_KEY_TEST="<value>" --app fgen
heroku config:set STRIPE_WEBHOOK_SECRET_TEST="<value>" --app fgen
heroku config:set PRODUCT_PRICE="<value>" --app fgen
heroku config:set PRODUCT_ID="<value>" --app fgen
heroku config:set REDIRECT_DOMAIN=https://www.fgen.ca --app fgen
```

`DATABASE_URL` is already injected automatically by the Heroku Postgres add-on — don't set it
manually unless you're pointing at a different database.

Verify what's set at any time with:
```bash
heroku config --app fgen
```

### 5. Release process (runs automatically via the Procfile)

The `Procfile` already runs `python manage.py migrate` on every release, so the new
`Executive`/`GoogleForm` tables will be created automatically on deploy. No manual step needed.

### 6. Post-deploy checks

```bash
heroku logs --tail --app fgen        # watch for startup errors
heroku ps --app fgen                 # confirm the web dyno is up
heroku open --app fgen               # opens the live site
```

Then in the browser, spot-check the same pages as the local checklist above, plus:
- Submit the Contact Us form on the live site and confirm no error page appears.
- Log into `/admin/` and confirm you can:
  - Add/edit **Executives** (About Us → Executives section)
  - Edit **WebData** entries for Programs page content (`programs_page_title`,
    `programs_card1_title`, `programs_card1_body`, `programs_card2_title`, `programs_card2_body`)
  - Edit **WebData** → `executive_applications_description` (Get Involved page text)
  - Add **Google Forms** with keys `programs_booking` and `executive_applications`, pasting in
    the form URLs from the spec document

---

## 4. Populating the new admin content (one-time, after first deploy)

These aren't seeded automatically — an admin needs to fill them in once via `/admin/`:

1. **Programs → Google Forms** → add one with key `programs_booking`, title
   `FGEN School Presentation Booking Form`, and the booking form URL.
2. **Get Involved → Google Forms** → add one with key `executive_applications`, title
   `FGEN Executive Applications`, and the applications form URL.
3. **Executives** → add up to 5 profiles (name, description, photo), mirroring how Leadership
   entries are set up.
4. Optionally override `programs_page_title` / `programs_card1_*` / `programs_card2_*` and
   `executive_applications_description` in **WebData** if the shipped defaults need tweaking —
   otherwise the code-level defaults already match the spec.

---

## Notes for future cleanup (not done in this pass, flagging for visibility)

- `db.sqlite3` and a few `__pycache__/*.pyc` files are tracked in git despite being listed in
  `.gitignore` — they were committed before the ignore rules existed. Untracking them
  (`git rm --cached db.sqlite3`) would be a good follow-up, but wasn't done here to avoid an
  unrequested destructive-looking change.
- Consider scrubbing the old plaintext secrets from git history (e.g. `git filter-repo`) once
  they're rotated — removing them from the *current* file doesn't remove them from history that's
  already public on GitHub.
