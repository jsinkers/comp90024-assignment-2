# comp90024-assignment-2

## view

### dependencies

* couchdb-python
 - pip install couchdb
* requests
 - pip install requests

### usage

You can import couchback in your code to use following functions.
`ci = CouchInterface()
view = ci.create_regex_view([args])`
More information is shown in the test cases below `if __name__ == '__main__'` and in the docstring of each method.

## database

- Contains ansible playbook for initialising 3 VMs and installing dependencies for couchDB.
- Cluster configuration is currently manual.
- Store the `openRC.sh` from the Melbourne Research Cloud into this directory
 
From this directory, to run the playbook, use:

```bash
./run-database.sh
```

