# COMP90024 Assignment 2: Livability in Melbourne

- install python dependencies using `pip install -r modules.txt`
 
## Docker

`Dockerfile` can be used to create a docker image of the twitter harvester

## Database - Ansible Playbook 

- Directory `database`
- Contains ansible playbook for initialising 3 VMs and installing dependencies for couchDB.
- Cluster configuration is currently manual.
- Store the `openRC.sh` from the Melbourne Research Cloud into this directory
 
From this directory, to run the playbook, use:

```bash
./run-database.sh
```

## Twitter Harvester 

- Directory `data_harvest`
- contains Twitter data harvesters
  - `harvest.py`: uses Twitter filter streaming API
  - `searchTwitter.py`: uses Twitter 30 day search API 
- configure info in `INFO.py`

## Flask 

- Directory `flask`
- Serves the frontend and ReST API
- before running the development server you need to build the frontend
- to run the development server: `flask run`
- alternatively can run with gunicorn from : `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

## Frontend

- Directory `frontend`
- This is a `svelte` app
- in `frontend` run `npm install` to install dependencies
- to build the app run `npm run build`