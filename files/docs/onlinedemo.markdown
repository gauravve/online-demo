# Welcome to the Deployit online demo! #

Script:

* log in
* visit release dashboard
** check PetPortal, PetClinic-ear, PetPortal
* deploy PetPortal/1.0 to TEST
* upgrade to PetPortal/2.0
* undeploy PetPortal
* reports
* log out

# Logging in #

Let's start by logging into Deployit. Open a browser with a Flash plugin and navigate to the URL provided in the online demo email. You will be presented with a login screen:

xxx

Enter the administrator credentials you received into the username and password fields and click the button.

You will now see the main Deployit user interface:

xxx

Along the top, you'll find the main areas in the Deployit GUI:

* **Deployment** where you can configure and execute deployments
* **Release Dashboard** where you can get an overview the applications you work with and where they are deployed
* **Repository** where you can see and edit the contents of the Deployit repository
* **Reports** where you can find reports about your deployment history
* **Admin** where you can configure security

In the top-right corner, you will find a a dropdown menu that offers access to the in-tool help, online documentation and support site. You can use these at any point in your demo to find more information.

Let's start by taking a look at what the demo environment looks like.

# The Release Dashboard #

Click on the Release Dashboard tab in the navigation bar. You'll see a release dashboard, currently empty:

xxx

The release dashboard is used to get an overview of all the versions of an application and where they are deployed. The left-hand side of the screen shows an application browser with all applications in the Deployit repository. Click on the `PetPortal` application to bring it up in the release dashboard:

![Release Dashboard - Deployment Pipeline](images/release-dashboard-deployment-pipeline.png "Release Dashboard - Deployment Pipeline")

This is called the `deployment pipeline` for the `PetPortal` application. It shows all environments the application journeys through (in this case, DEV, TEST, ACC and PROD) and which versions of the application are currently deployed where.

You can bring up more applications by clicking on them in the application browser.

To zoom in on a particular application version, select it from either the application browser or click on the version number in the deployment pipeline. Try it now by clicking on the **_1.0_** version in the `PetPortal` deployment pipeline:

![Release Dashboard - Application Version](images/release-dashboard-application-version.png "Release Dashboard - Application Version")

Here, you see that `PetPortal` version `1.0` is deployed to the DEV environment. This version can also be deployed to the TEST environment (indicated by the green border and **deploy** icon). The ACC and PROD environments are currently off-limits for this version. Click on the **_PROD_** environment to see which conditions apply:

![Release Dashboard - Environment Conditions](images/release-dashboard-environment-conditions.png "Release Dashboard - Environment Conditions")

The PROD environment requires that the package has release notes (the `1.0` version of `PetPortal` satisfies this condition) and that it is both performance tested and has a change ticket number. Neither of the latter two conditions is currently satisfied, which is why this version can not be deployed to PROD.

To move our `PetPortal` 1.0 application further along it's deployment pipeline, let's deploy it to the TEST environment. Click on the deployment icon (parachute) in the TEST environment box to start.

# Deploying PetPortal to TEST #

This brings up the deployment screen that was open when Deployit started. This time, though, it looks like this:

![Deployment - PetPortal 1.0 to TEST](images/deployment-petportal-1.0-to-TEST.png "Deployment - PetPortal 1.0 to TEST")

The central part of this screen shows the deployment we have just started -- PetPortal/1.0 to the TEST environment. Because there is currently no version of PetPortal deployed to the environment, this is called an _initial_ deployment.

The `PetPortal/1.0` package we want to deploy is shown in the left box. Here, you can see which Configuration Items (CIs for short) are part of this application package. The package consists of everything the PetPortal application needs to run. That includes artifact CIs (`PetClinic-ear`, an EAR file or `sql`, a folder of SQL scripts for the database) and resource CIs (`PetClinic-ds-on-jboss`, a datasource or `PetPortal-host`, an Apache virtual host).

The right box shows the TEST environment. It consists of a number of containers that we can deploy to: `TEST-Apache`, an apache webserver, `TEST-AppServer`, a JBoss application server and `TEST-MySql`, a database.

Before we can deploy our application, we need to tell Deployit which components of the PetPortal/1.0 package should be deployed to which members of the environment. We can do this by hand, by dragging and dropping the individual package members to the environment members, but there is a better way. 

Based on the types of package members and environment members, Deployit can figure out which members should go where. Click on the Automap arrow (the double arrow in the top of the left box) to let Deployit figure this out:

![Deployment - PetPortal 1.0 to TEST - mappings](images/deployment-petportal-1.0-to-TEST-mappings.png "Deployment - PetPortal 1.0 to TEST - mappings")

As you can see, Deployit managed to map all of our package members to members of the environment: webserver configuration and HTML to the apache host, the datasource and EAR file to the application server and the SQL files to the database. There is also a `TestRunner` member in the environment which we'll talk about later.
