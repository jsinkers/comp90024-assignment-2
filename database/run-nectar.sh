#!/bin/bash

. ./openrc.sh; ansible-playbook nectar.yaml -u ubuntu --key-file=~/.ssh/database.pem