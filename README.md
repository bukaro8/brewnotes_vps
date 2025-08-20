run  docker compose exec web  python manage.py  makemigrations
run  docker compose exec web  python manage.py  migrate     
create and empty migration to preload data   
 docker compose exec web python manage.py makemigrations --empty notes --name load_initial_data
Edit notes/migrations/0002_load_initial_data.py
for static/global/data/data.py this file contains data to feed your app (this step is optional but recomended)


Header/Navbar: Hop Green #5B8C3A + #F8F5F0 Off-White text.

Buttons: Malt Gold #D4A017 with dark text.

Links/Interactive: Fermentation Purple #6A4C93.

Cards/Forms: Warm Gray #D3CEC4 border on Off-White.
# 🍺 BrewNotes — Homebrew Recipe & Batch Tracker
![App Screenshot](documentation/app-screenshot.jpg)
🐛 Bugs & Solutions
| Bug                       | Symptom                                | Solution                                                                                       | Impact                    |
| ------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------- |
| Static Manifest Errors    | 500 after enabling WhiteNoise manifest | Switched to `CompressedStaticFilesStorage` + re-collect                                        | Static serving stabilized |
| OAuth Redirect Using HTTP | Google “request invalid”               | Set `ACCOUNT_DEFAULT_HTTP_PROTOCOL=https`, proxy headers, Gunicorn `--forwarded-allow-ips="*"` | OAuth working in prod     |
| Port 80 Conflict          | Caddy failed to bind                   | Stopped Apache & remapped any other services                                                   | HTTPS live                |
| PgAdmin Public Exposure   | Port 80/5050 accessible publicly       | Bound to `127.0.0.1:5050` + SSH tunnel                                                         | Safer admin access        |
