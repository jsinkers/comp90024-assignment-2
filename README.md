# comp90024-assignment-2

## view

### Dependencies

* couchdb == 1.2  
* requests == 2.27.1  
* shapely == 1.6.4.post1  
* pandas == 1.3.5

### Usage

You can import couchback in your code to use following functions.
`ci = CouchInterface()
view = ci.create_regex_view([args])`
More information is shown in the test cases below `if __name__ == '__main__'` and in the docstring of each method.

### Modules

* couchback  
It has two classes `CouchInterface` and `MapGenerator`. The first one is used to connect to a couchdb database, create views, and get the views. 
The second one can be used to quickly generate a JavaScript map function.
* preprocess  
In this module, some functions listed to get common used views. You can create your own design documents to get custom views like the examples, but you must not use the same design name. Note that you cannot use a same design name to overwrite a design document with it.

## database

- Contains ansible playbook for initialising 3 VMs and installing dependencies for couchDB.
- Cluster configuration is currently manual.
- Store the `openRC.sh` from the Melbourne Research Cloud into this directory
 
From this directory, to run the playbook, use:

```bash
./run-database.sh
```

