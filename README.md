# phraseGen
Random phrase generator

Install `virtualenv`

Install `ngnix`

Commands

	- virtualenv pg

	- pip install -r requirements.txt

Copy assets to ngnix HTML folder

Edit phraseGen.py to point to ngnix server

Run `gunicorn --bind 0.0.0.0:8000 phraseGen:application --reload`