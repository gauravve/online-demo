# Introduction #

This Vagrant project sets up a demo of Deployit using the PetPortal application using Apache2, JBoss 5 and MySql and the maven plugin.

# Getting dependencies #

You'll need the following dependencies available to run the demo:

* deployment-test2-plugin-1.0-milestone-7.jar
* jboss-5.1.0.GA.zip

Puppet will download the Deployit server and CLI, JBoss and WLS plugins from Nexus.

# Starting the demo #

To start all 4 images:

    sudo vagrant up

To start each of the images separately:

    sudo vagrant up deployit
    sudo vagrant up web    
    sudo vagrant up app    
    sudo vagrant up db    

## Access the instance ##

Visit URL http://localhost:4516 .

# Demo scenario #

* import the PetPortal application, version 1 and 2
* deploy PetPortal/1.0 to DEV, skip all steps (DEV environment doesn't work)
* deploy PetPortal/1.0 to TEST
* execute the deployment
* PetPortal URL: http://192.168.1.11/
* upgrade PetPortal/2.0 on TEST -- this website content contains an intentional typo
* use the maven plugin project (mvn deployit:deploy) to create a new DAR, execut the deployment & fix the typo
