import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

## Function for Filtering the instances based on project
def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances= ec2.instances.all()
    return instances

@click.group()
def cli():
    "Shotty manages snapshots"

@cli.group('snapshots')
def snapshots():
    "Commonds for snapshots"

## Display list of instances for the project
@snapshots.command('list')
@click.option('--project',default=None,
    help="Only volumes for project (tag Project:<name>)")
def list_snapshots(project):
    "List Snapshots in all EC2 instances"
    
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    i.id,
                    v.id,
                    s.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

@cli.group('volumes')
def volumes():
    "Commands for volumes"

## Display list of instances for the project
@volumes.command('list')
@click.option('--project',default=None,
    help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List Volumes of EC2 instances"
    
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
            i.id,
            v.id,
            v.stat,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted" )))
    return

@cli.group('instances')
def instances():
    "Commands for instances"

## Display list of instances for the project
@instances.command('list')
@click.option('--project',default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    
    instances = filter_instances(project)
    for i in instances:
        tags = { t['Key']:t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>') )))
    return

## Create Snapshots for all instances in the project project
@instances.command('snapshot')
@click.option('--project',default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshot for EC2 instances"
    
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshots(Description="Created by Snapshotalyzer")
    return

## Stop the EC2 instances related for the project
@instances.command('stop')
@click.option('--project',default=None,
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0} ....".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project',default=None,
    help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Starting {0} ....".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    cli()
    

    