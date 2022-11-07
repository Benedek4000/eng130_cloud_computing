# Networks

## Definitions

### VPC

A virtual private cloud is an environment within a public cloud. It is isolated
from the public cloud to provide a virtual private environment.

![vpc diagram](https://github.com/Benedek4000/eng130_cloud_computing/blob/main/images/vpc.png)

### IG

An internet gateway is a VPC component that allows communication between the 
VPC and the internet.

### RT

A route table contains the available route targets. It is a set of rules
to determine where information travels within the given network.

### CIDR blocks

A CIDR (classless inter-domain routing) block is essentially and IP address
range. A VPC can have two CIDR blocks (for IPv4 and IPv6).

### Subnet

A subnet is a range of IP addresses within a network, to which instances 
can be attached.

### NACLs

A network access control list is an extra security layer for a VPC, allowing 
traffic in and out of the given subnet(s). It is optional.

## NACL vs SG

NACLs are layers of security for a subnet, while SGs are layers of security
for a given instance.

