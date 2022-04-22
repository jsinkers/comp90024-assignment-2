#!/bin/bash -v

# first script to run
# using verbose output

# set up environment variables
# get external IP address
# based on https://stackoverflow.com/questions/13322485/how-to-get-the-primary-ip-address-of-the-local-machine-on-linux-and-os-x
export node=$(ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
echo "Node: ${node}"

#export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
#export size=${#nodes[@]}
export user='admin'
export pass='comp90024-password'
export VERSION='3.2.1'
export cookie='a192aeb9904e6590849337933b000c99'
export contname=couchdb${node}
echo "Container name: ${contname}"

# pull the couchdb image
docker pull ibmcom/couchdb3:${VERSION}

# stop and remove any current container
if [ ! -z $(docker ps --all --filter "name=${contname}" --quiet) ] 
    then
        docker stop $(docker ps --all --filter "name=${contname}" --quiet) 
        docker rm $(docker ps --all --filter "name=${contname}" --quiet)
fi 

# create docker containers
#--name couchdb${node}\
docker create\
    --name ${contname} \
    --env COUCHDB_USER=${user} \
    --env COUCHDB_PASSWORD=${pass} \
    --env COUCHDB_SECRET=${cookie} \
    --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"${contname}\"" \
    -p 5984:5984 \
    -p 5984:5984 \
    -p 9100:9100 \
    ibmcom/couchdb3:${VERSION}

# start the containers
docker start ${contname}

