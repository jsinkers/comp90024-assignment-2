#!/bin/bash
echo "Enter docker hub password for sinkers"
read -sr PASSWORD_INPUT

. ./openrc.sh; ansible-playbook deploy-flask.yaml -u ubuntu --key-file=~/.ssh/database.pem --extra-vars 'dockerhub_password: $PASSWORD_INPUT'
