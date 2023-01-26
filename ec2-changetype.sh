#!/bin/bash

# Check if two arguments were provided (instance name and instance type)
if [ $# -ne 2 ]; then
  echo "Error: Please provide the instance name and instance type as arguments."
  exit
fi

# Set variables for the instance name and instance type
INSTANCE_NAME=$1
INSTANCE_TYPE=$2

# Find the instance ID using the instance name
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=$INSTANCE_NAME" --query "Reservations[*].Instances[*].InstanceId" --output text)

# Stop the instance
aws ec2 stop-instances --instance-ids $INSTANCE_ID

# Wait for the instance to stop
aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID

# Change the instance type
aws ec2 modify-instance-attribute --instance-id $INSTANCE_ID --instance-type "{\"Value\": \"$INSTANCE_TYPE\"}"

# Start the instance
aws ec2 start-instances --instance-ids $INSTANCE_ID

# Wait for the instance to start
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

echo "Instance $INSTANCE_NAME with ID $INSTANCE_ID has been stopped, had its instance type changed to $INSTANCE_TYPE, and has been started again."
