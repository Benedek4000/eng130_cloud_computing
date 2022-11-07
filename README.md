# Cloud Computing with AWS

## What is cloud computing?

Cloud computing is the delivery of computational and non-computational
resources over the internet. Instead of owning the equipment used by a company,
including servers, data centers and much more, a cloud provider provides these
services to the company. One of these cloud providers is Amazon, 
with Amazon Web Services (AWS).

### Benefits

- Ease of Use
- Flexibility
- Robustness
- Cost: Pay As You Go

### What is AWS?

AWS is an Amazon product, which provides cloud computing tools, 
such as platforms and APIs.

### PAAS vs. SAAS vs. IAAS

- PAAS: Platform-as-a-Service
- SAAS: Software-as-a-Service
- IAAS: Infrastructure-as-a-Service

![PAAS vs. SAAS vs. IAAS diagram](https://www.redhat.com/cms/managed-files/iaas-paas-saas-diagram5.1-1638x1046.png)

### CapEx vs. OpEx

- CapEx: Major purchases a company makes, designed for long term usage
- OpEx: Day-to-Day expenses incurred

![CapEx vs. OpEx diagram](https://forcam.com/app/uploads/2021/08/capex_opex-comparison-750x0-c-default.jpg)

## Setting up a VM in AWS

### SSH key

- copy ssh key into .ssh folder
- `chmod 400 [key name].pem`

### Setting up the VM

- launch EC2
- name instance (eg. eng130-benedek)
- os: Ubuntu 18.04
- type: t2.micro
- key pair: eng130
- allow for ssh and http
- create security convention or use an already existing one
- click 'Launch instance'
- ssh into VM using the connect tab
- run a set of provisions, eg.:
```commandline
sudo apt update
sudo apt upgrade -y
sudo apt install nginx -y
sudo systemctl enable nginx
```

### Set up reverse proxy

- `sudo nano /etc/nginx/sites-available/default`
- add the following inside location:
```other
proxy_pass http://localhost:3000;
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection 'upgrade';
proxy_set_header Host $host;
proxy_cache_bypass $http_upgrade;
```
- restart nginx: `sudo systemctl restart nginx`

### Setup nodejs app

```commandline
sudo apt-get install python -y
sudo apt-get install software-properties-common -y
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install nodejs -y
sudo npm install pm2 -g
# navigate to the app folder
sudo npm install
sudo systemctl restart nginx
npm start
```

## 2-tier architecture

![2-tier architecture diagram](https://github.com/Benedek4000/eng130_cloud_computing/blob/main/images/2tier.png)

### MongoDB setup

on AWS, allow access for the app vm by editing the security groups

install mongodb:
```commandline
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```

in `/etc/mongod.conf` edit bind ip to localhost

setup mongodb:
```commandline
sudo systemctl enable mongod
sudo systemctl restart mongod
```

### App setup

see above, but run
```commandline
export DB_HOST=mongodb://[db_ip]:[db_port]/[db_name]
node seeds/seed.js
npm start
```

## Disaster recovery

Disaster recovery (DR) is a set of policies and procedures in place to 
enable the recovery of a system, in case in goes down or becomes unavailable.

### S3

Amazon S3 offers features to improve data resilience and provide backup 
in case of a disaster. Amazon S3 is capable of transferring and storing
objects and data to less expensive storage.

![amazon s3 diagram](https://github.com/Benedek4000/eng130_cloud_computing/blob/main/images/amazons3.png)

### Benefits

- backups can be made
- less expensive
- more resilient data
- objects can be restored in case of a disaster

### Use cases of disaster recovery

- natural disaster hits the primary site, eg. tornado or tsunami
- a copy of the primary site needs to be opened, eg. the company is scaling up
- human disaster hits the primary site, eg. cyber attack or negligence
- hardware failure, eg. physical damage or fire

## AWSCLI

to connect to awscli, use the following commands:

```commandline
sudo apt update
sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
alias python=python3
sudo pip3 install awscli
aws configure  # then follow the instructions
# enter access key and secret access key
# enter region and output format (eg. eu-west-1 & json)
aws s3 ls  # to check access & list s3 buckets available
```

## Auto-Scaling Groups (ASGs)

ASGs are groups of instances, which automatically scale with the needs of the
business, by creating and destroying instances to provide resources for the
needs of the business.

![asg diagram](https://github.com/Benedek4000/eng130_cloud_computing/blob/main/images/asg.png)

### Benefits

- cost
- resilience
- reliability

### Creating an ASG

in AWS:
- create a launch template, by defining the basic properties of th instances 
created by the auto-scaling group
- make sure to create a security group for the template, as the instances
can be identified by this security group, in case they need to connect to
another instance (like a database host)
- load-balancing can be used to set up exactly when the ASG should create
or destroy instances
- to provide a provision script, edit the user data in advanced details, 
make sure to include `#!/bin/bash` as the first line
- once the template is created, create a new auto-scaling group based on the 
template created
- in a few minutes, the first instances should be created

### Creating an alarm

in AWS:
- add ASG to a dashboard
- in the dashboard, create an alarm, by specifying the conditions for the 
alarm to trigger and by setting up an alarm group, the members of which 
would receive the alarm when triggered