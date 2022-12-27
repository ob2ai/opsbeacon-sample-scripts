#!/bin/bash

# Check if at least one argument was provided
if [ $# -eq 0 ]
then
    echo "Error: No container name(s) provided"
    exit
fi

# Loop through each container name passed as an argument
for container in "$@"
do
    # Check if the container name is empty or contains any special characters
    if [ -z "$container" ] || ! [[ "$container" =~ ^[a-zA-Z0-9._-]+$ ]]
    then
        echo "Error: Invalid container name: $container"
        continue
    fi

    # Check if the container exists
    if ! docker inspect "$container" &> /dev/null
    then
        echo "Error: Container does not exist: $container"
        continue
    fi

    # Check if the container is running
    if [ "$(docker inspect -f '{{.State.Running}}' "$container")" = "true" ]
    then
        # Stop the container
        docker stop "$container"

        # Wait for the container to fully stop
        while [ "$(docker inspect -f '{{.State.Running}}' "$container")" = "true" ]
        do
            sleep 1
        done
    fi
done
