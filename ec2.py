#!/usr/bin/env python3

from time import strftime
from opsbeacon import *

import argparse
import json

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--list', action='store_true', help="List all EC2 instances")
    parser.add_argument('--instance-id', '-i', nargs="+", default=[], help="EC2 instance ID")
    parser.add_argument('--region', '-r', help="AWS region")
    parser.add_argument('--stop', '-p', action='store_true', help="Stop EC2 instance")
    parser.add_argument('--start', '-t', action='store_true', help="Start EC2 instance")
    parser.add_argument('--terminate', '-e', action='store_true', help="Terminate EC2 instance")
    parser.add_argument('--reboot', '-b', action='store_true', help="Reboot EC2 instance")
    parser.add_argument('--status', '-u', action='store_true', help="Display the status of an EC2 instance")

    args = parser.parse_args()

    report = []

    if args.list:
        report = action_list_ec2_instances(args)
        json_data = json.dumps(report, indent=4)
        csv_data = json2csv(json_data)
        print(csv_data)
        print(f"Added {len(report)} EC2 instances to the report")
    
    if args.stop:
        action_stop_ec2_instances(args)
    
    if args.start:
        action_start_ec2_instances(args)

    if args.terminate:
        action_terminate_ec2_instances(args)

    if args.reboot:
        action_reboot_ec2_instances(args)
    
    if args.status:
        action_status_ec2_instances(args)

if __name__ == "__main__":
    main()
