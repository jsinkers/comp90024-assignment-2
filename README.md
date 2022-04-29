# COMP90024 Assignment 2: Livability in Melbourne

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
