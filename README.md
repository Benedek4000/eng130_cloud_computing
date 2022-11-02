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
