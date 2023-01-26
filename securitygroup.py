import boto3
import argparse


def get_security_group(group_name):
    # Create a client for EC2
    ec2 = boto3.client('ec2')

    # Get the security group with the given name
    security_groups = ec2.describe_security_groups(Filters=[{'Name': 'tag:Name', 'Values': [group_name]}])
    if security_groups['SecurityGroups']:
        return security_groups['SecurityGroups'][0]
    else:
        raise ValueError(f"Security group with name {group_name} not found.")

def list_rules(group_name):
    security_group = get_security_group(group_name)
    for i, rule in enumerate(security_group['IpPermissions']):
        cidrs = []
        for ip_range in rule['IpRanges']:
            cidrs.append(ip_range['CidrIp'])
        print(f"{i+1}. {rule['IpProtocol']} {rule['FromPort']} - {rule['ToPort']} {cidrs}")
    
def add_rule(group_name, port, source_cidr, proto="tcp"):
    security_group = get_security_group(group_name)
    ec2 = boto3.client('ec2')
    response = ec2.authorize_security_group_ingress(
        GroupId=security_group['GroupId'],
        IpPermissions=[
            {
                'FromPort': int(port),
                'ToPort': int(port),
                'IpProtocol': proto,
                'IpRanges': [
                    {
                        'CidrIp': source_cidr,
                    },
                ],
            },
        ],
    )
    print(f"Added rule for port {port} from source CIDR {source_cidr} to security group {group_name}")

def remove_rule(group_name, rule_id):
    security_group = get_security_group(group_name)
    ec2 = boto3.client('ec2')
    ec2.revoke_security_group_ingress(
        GroupId=security_group['GroupId'],
        IpPermissions=[
            security_group['IpPermissions'][int(rule_id)]
        ]
    )
    print(f"Removed rule {rule_id} from security group {group_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('group_name', type=str, help='The name of the security group')
    parser.add_argument('--list', action='store_true', help='List all rules for the given security group')
    parser.add_argument('--add', nargs=2, metavar=('port', 'source_cidr'), help='Add a rule for the given port and source CIDR')
    parser.add_argument('--remove', type=int, help='Remove the rule with the given ID')
    args = parser.parse_args()

    if args.list:
        list_rules(args.group_name)
    elif args.add:
        port, source_cidr = args.add
        add_rule(args.group_name, port, source_cidr)
    elif args.remove:
        rule_id = args.remove - 1
        remove_rule(args.group_name, rule_id)
    else:
        parser.print_help()
