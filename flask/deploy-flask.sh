#!/bin/bash
echo "Enter docker hub password for sinkers"
read -sr PASSWORD_INPUT
. ./openrc.sh; ansible-playbook database.yaml -u ubuntu --key-file=~/.ssh/database.pem --extra_vars "dockerhub_password: $PASSWORD_INPUT"
