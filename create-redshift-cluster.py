import logging
import argparse
import boto3
import os
import configparser

# CONFIG
CONFIG_FILE = 'redshift.cfg'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

KEY = os.environ['AWS_SECRET_ACCESS_KEY']
SECRET = os.environ['AWS_ACCESS_KEY_ID']
REGION = config['REDSHIFT']['REGION']

DWH_IAM_ROLE_NAME = config['REDSHIFT']['IAM_ROLE_NAME']


def create_resources():
    """ create resources """
    options = dict(region_name=REGION, aws_access_key_id=KEY, aws_secret_access_key=SECRET)
    ec2 = boto3.resource('ec2', **options)
    s3 = boto3.resource('s3', **options)
    iam = boto3.client('iam', **options)
    redshift = boto3.client('redshift', **options)
    return ec2, s3, iam, redshift

def create_iam_role(iam):
    """ Create IAM role for Redshift cluster """
    try:
        dwh_role = iam.create_role(
            Path = '/',
            RoleName = 'DWH_IAM_ROLE_NAME',
            AssumeRolePolicyDocument=json.dumps({
                'Statement': [{
                    'Action': 'sts:AssumeRole',
                    'Effect': 'Allow',
                    'Principal': {'Service': 'redshift.amazonaws.com'}
                }],
                'Version': '2012-10-17'
            })
        )
        iam.attach_role_policy(
            RoleName=DWH_IAM_ROLE_NAME,
            PolicyArn=S3_READ_ARN
        )
    except ClientError as e:
        logging.warning(e)

    role_arn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
    logging.info('Role {} with arn {}'.format(DWH_IAM_ROLE_NAME, role_arn))
    return role_arn

def create_redshift_cluster(redshift, role_arn):
    """ Create Redshift cluster """
    try:
        redshift.create_cluster(
            ClusterType = config['REDSHIFT']['CLUSTER_TYPE'],
            NodeType = config['REDSHIFT']['NODE_TYPE'],
            ClusterIdentifier = config['REDSHIFT']['CLUSTER_IDENTIFIER']


        )

def main(args):
    ''' Main function '''
    ec2, iam, s3, redshift = create_resources()

    logging.info('Started in main ...')
    if args.delete:
        delete_redshift_cluster(redshift)
        delete_iam_role(iam)
        return

    role_arn = create_iam_role(iam)
    create_redshift_cluster(redshift, role_arn)
    config['REDSHIFT']['IAM_ROLE_ARN'] = role_arn

    # Poll the Redshift cluster after creation until available




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting in main ...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--delete', dest='delete', default=False, action='store_true')
    parser.add_argument('--query_file', dest='query_file', default=None)
    args = parser.parse_args()
    print(args.delete)
    main(args)