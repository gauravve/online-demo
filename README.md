# Introduction #

This project sets up the Deployit 3.9 online demo. It is meant to be run from a newly provisioned Amazon EC2 image.

# Preparation of the AMI #

Tools:

* yum update
* yum install git puppet
* change /etc/ssh/sshd_config:
** PasswordAuthentication yes
** PermitEmptyPasswords no
* curl https://raw.github.com/timkay/aws/master/aws -o aws (to download the Deployit binaries from S3, see http://timkay.com/aws/)
* https://github.com/alue/markdown-handler (to render the markdown online demo docs)

Our stuff:

* cd /etc/puppet
* git clone git://github.com/xebialabs/online-demo.git
* install dependencies (see below)
* puppet apply --modulepath /etc/puppet/online-demo/modules /etc/puppet/online-demo/manifests/database.pp
* puppet apply --modulepath /etc/puppet/online-demo/modules /etc/puppet/online-demo/manifests/webserver.pp
* puppet apply --modulepath /etc/puppet/online-demo/modules /etc/puppet/online-demo/manifests/appserver.pp

# Starting the demo #

* puppet apply --modulepath /etc/puppet/online-demo/modules /etc/puppet/online-demo/manifests/deployit.pp

There is an init script at 

# Dependencies #

You'll need the following dependencies to run the demo:

* deployit-server.zip
* deployit-cli.zip
* jbossas-plugin.jar
* deployment-test2-plugin-1.0-milestone-7.jar
* jboss-5.1.0.GA.zip (from http://downloads.sourceforge.net/project/jboss/JBoss/JBoss-5.1.0.GA/jboss-5.1.0.GA.zip)

They are stored in an S3 bucket *deployit-online-demo*.

# Provisioning a demo #

* launch a Large instance from our Online Demo AMI
* wait until it is up
* copy the public DNS name
* try to access http://PUBLIC_DNS_NAME:4516/

# How it works #

The AMI already contains all required middleware to be able to run the demo. When it starts, the httpd server, jboss and mysql are all started through init scripts.

Quirks:

* the downloaded files end up in directory /download-cache to keeps things in sync with our current vagrant setup.
* the directory /demo-files on the AMI is also used, it is a symlink to the files directory in this project.

# Accessing the demo #

To access the Deployit server, visit http://PUBLIC_DNS_NAME:4516/

Username/password: admin/admin

Documentation can be found at http://PUBLIC_DNS_NAME/online-demo/

# Demo email #

When a customer requests a demo, send him/her an email with the following content:

	Dear Deployit customer,

	thank you for requesting a Deployit demo!

	xxx

	These are the addresses and credentials you will need:

	Deployit online demo: *specify URL*
	Deployit username: *specify username*
	Deployit password: *specify password*

	Deployit online demo scenario: *specify URL*

	The demo makes use of some middleware, namely an apache webserver, JBoss application server and MySQL database. You can access the webserver on *specify URL*.



	We hope you enjoy learning about the Deployit application release automation solution. If you have any questions or run into problems, please contact us at http://support.xebialabs.com.


	Sincerely,

	XebiaLabs
