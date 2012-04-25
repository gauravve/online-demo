# Introduction #

This project sets up the Deployit online demo. It is meant to be run from a newly provisioned Amazon EC2 image.

# Overall setup #

* 

# Preparation of the AMI #

* yum update
* yum install git puppet
* change /etc/ssh/sshd_config:
** PasswordAuthentication yes
** PermitEmptyPasswords no
* cd /etc/puppet
* git clone git://github.com/xebialabs/online-demo.git
* install dependencies (see below)
* puppet apply --modulepath /etc/puppet/online-demo/modules /etc/puppet/online-demo/manifests/init.pp

# Getting dependencies #

You'll need the following dependencies available in /download-cache to run the demo:

* deployit-server.zip
* deployit-cli.zip
* jbossas-plugin.jar
* deployment-test2-plugin-1.0-milestone-7.jar
* jboss-5.1.0.GA.zip (from http://downloads.sourceforge.net/project/jboss/JBoss/JBoss-5.1.0.GA/jboss-5.1.0.GA.zip)

# Accessing the demo #

To access the Deployit server, visit http://<EC2 public DNS name>:4516/

Username/password: admin/admin
