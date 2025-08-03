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