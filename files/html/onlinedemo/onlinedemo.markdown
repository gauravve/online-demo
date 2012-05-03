# Welcome to the Deployit online demo! #

Welcome to the Deployit online demo. This demo will give you a feel for the Deployit product and allows you to play around with it in a "safe" environment.

To help you get started, we've provided this scripted scenario that takes you through a deployment, upgrade and undeployment with Deployit.

# Logging in #

Let's start by logging into Deployit. Open a browser with a Flash plugin and navigate to the URL provided in the online demo email. You will be presented with a login screen:

![Deployit Login](images/deployit-login.png "Deployit Login")

Enter the administrator credentials you received into the username and password fields and click the button.

You will now see the main Deployit user interface:

![Deployit first screen](images/deployit-first-screen.png "Deployit first screen")

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

![Release Dashboard](images/release-dashboard.png "Release Dashboard")

The release dashboard is used to get an overview of all the versions of an application and where they are deployed. The left-hand side of the screen shows an application browser with all applications in the Deployit repository. Click on the `PetPortal` application to bring it up in the release dashboard:

![Release Dashboard - Deployment Pipeline](images/release-dashboard-deployment-pipeline.png "Release Dashboard - Deployment Pipeline")

This is called the _deployment pipeline_ for the `PetPortal` application. It shows all environments the application journeys through (in this case, DEV, TEST, ACC and PROD) and which versions of the application are currently deployed where.

You can bring up more applications by clicking on them in the application browser.

To zoom in on a particular application version, select it from either the application browser or click on the version number in the deployment pipeline. Try it now by clicking on the **_1.0_** version in the `PetPortal` deployment pipeline:

![Release Dashboard - Application Version](images/release-dashboard-application-version.png "Release Dashboard - Application Version")

Here, you see that `PetPortal` version `1.0` is deployed to the DEV environment. This version can also be deployed to the TEST environment (indicated by the green border and **deploy** icon). The ACC and PROD environments are currently off-limits for this version. When you click on the **_PROD_** environment you can see why this is the case:

![Release Dashboard - Environment Conditions](images/release-dashboard-environment-conditions.png "Release Dashboard - Environment Conditions")

The PROD environment requires that the package has release notes (the `1.0` version of `PetPortal` satisfies this condition) and that it is both performance tested and has a change ticket number. Neither of the latter two conditions is currently satisfied, which is why this version can not be deployed to PROD.

To move our `PetPortal` 1.0 application further along it's deployment pipeline, let's deploy it to the TEST environment. Click on the deployment icon (parachute) in the TEST environment box to start.

# Deploying PetPortal 1.0 to TEST #

This brings up the deployment screen that was open when Deployit started. This time, though, it looks like this:

![Deployment - PetPortal 1.0 to TEST](images/deployment-petportal-1.0-to-TEST.png "Deployment - PetPortal 1.0 to TEST")

The central part of this screen shows the deployment we have just started -- PetPortal/1.0 to the TEST environment. Because there is currently no version of PetPortal deployed to the environment, this is called an _initial_ deployment.

The `PetPortal/1.0` package we want to deploy is shown in the left box. Here, you can see which Configuration Items (CIs for short) are part of this application package. The package consists of everything the PetPortal application needs to run. That includes artifact CIs (`PetClinic-ear`, an EAR file or `sql`, a folder of SQL scripts for the database) and resource CIs (`PetClinic-ds-on-jboss`, a datasource or `PetPortal-host`, an Apache virtual host). The members are all colored orange because they have not yet been mapped to members in the target environment.

The right box shows the TEST environment. It consists of a number of containers that we can deploy to: `TEST-Apache`, an apache webserver, `TEST-AppServer`, a JBoss application server and `TEST-MySql`, a database.

Before we can deploy our application, we need to tell Deployit which components of the PetPortal/1.0 package should be deployed to which members of the environment. We can do this by hand, by dragging and dropping the individual package members to the environment members, but there is a better way. 

Based on the types of package members and environment members, Deployit can figure out which members should go where. Click on the Automap arrow (the double arrow in the top of the left box) to let Deployit figure this out:

![Deployment - PetPortal 1.0 to TEST - mappings](images/deployment-petportal-1.0-to-TEST-mappings.png "Deployment - PetPortal 1.0 to TEST - mappings")

As you can see, Deployit managed to map all of our package members to members of the environment: webserver configuration and HTML to the apache host, the datasource and EAR file to the application server and the SQL files to the database. There is also a `TestRunner` member in the environment which we'll talk about later.

With the mappings in place, we can now customize the way Deployit deploys the components to their containers. Clicking a particular deployed item (or _deployed_ for short) in the right box will bring up the balloon editor in which you can edit the deployed's values. Try clicking on the `PetPortal-host` deployed:

![Deployment - PetPortal 1.0 to TEST - balloon](images/deployment-petportal-1.0-to-TEST-balloon.png "Deployment - PetPortal 1.0 to TEST - balloon")

The balloon shows the properties of the virtual host deployed that is mapped to the TEST-Apache webserver. This is how you can configure the deployment of the same resource to different containers.

Click the **Next** button to proceed with the deployment. Deployit will use the deployment package components and target environment makeup to calculate the required steps needed to execute the deployment. The steplist is also tailored to the current state of the middleware so that only the required steps and no more are executed. The final deployment plan is shown as a list of steps:

![Deployment - PetPortal 1.0 to TEST - steplist](images/deployment-petportal-1.0-to-TEST-steplist.png "Deployment - PetPortal 1.0 to TEST - steplist")

Before starting the deployment, you can review the steps that were generated. If you have the proper permissions, you can also skip steps and change the sequence of steps by dragging them to a different place in the list.

To start the deployment, click the **Deploy** button. Deployit will execute the deployment steps one by one, showing the logs:

![Deployment - PetPortal 1.0 to TEST - execution](images/deployment-petportal-1.0-to-TEST-execution.png "Deployment - PetPortal 1.0 to TEST - execution")

Once the deployment has finished successfully, the screen looks like this:

![Deployment - PetPortal 1.0 to TEST - completed](images/deployment-petportal-1.0-to-TEST-completed.png "Deployment - PetPortal 1.0 to TEST - completed")

Click the **Close** button to close the deployment window.

The PetPortal application is now available via the URL mentioned in the online demo email you received. This is what it looks like:

![PetPortal 1.0](images/petportal-1.0.png "PetPortal 1.0")

Now, let's check the Release Dashboard for final confirmation of the successful initial deployment to the TEST environment. This shows the following:

![Release Dashboard - PetPortal 1.0 on TEST](images/release-dashboard-petportal-1.0-on-TEST.png "Release Dashboard - PetPortal 1.0 on TEST")

# Upgrading PetPortal to 2.0 on TEST #

Now that PetPortal 1.0 is deployed to the TEST environment, let's see if we can upgrade it to 2.0. Bring up the Release Dashboard for this version by clicking on the **_2.0_** PetPortal version in the left-hand window:

![Release Dashboard - PetPortal 2.0](images/release-dashboard-petportal-2.0.png "Release Dashboard - PetPortal 2.0")

The green border around the TEST environment indicates we can deploy the 2.0 version there, too. Start the deployment by clicking on the **Deploy** icon. The deployment screen is show, loaded with the upgrade:

![Deployment - PetPortal 2.0 to TEST](images/deployment-petportal-2.0-to-TEST.png "Deployment - PetPortal 2.0 to TEST")

Note that the mappings we made during our previous deployment are all reused here so we don't have to configure anything. If the new version of PetPortal contained additional components or some components had been removed, we would have had to update the mappings on this screen. Because this is not the case, we can continue straight on to the steplist by clicking on the **Next** button:

![Deployment - PetPortal 2.0 to TEST - steplist](images/deployment-petportal-2.0-to-TEST-steplist.png "Deployment - PetPortal 2.0 to TEST - steplist")

The steplist is different this time. Deployit only generates steps for components that have changed since the last deployment. Because the datasource hasn't changed, there are no steps in the steplist to update it. The other components (EAR file, static content and database scripts) _have_ changed and so will be deployed again. Click the **Deploy** button to start the upgrade.

When the deployment completes, click the close button to close the window.

Now, our PetPortal page shows a new and improved PetPortal application:

![PetPortal 2.0](images/petportal-2.0.png "PetPortal 2.0")

# Undeploying PetPortal from TEST #

To completely remove the PetPortal application from the TEST environment, locate the PetPortal 2.0 deployment in the Deployed Application browser on the right-hand side of the Deployment screen:

![Undeployment - PetPortal 2.0 on TEST](images/undeployment-petportal-2.0-on-TEST.png "Undeployment - PetPortal 2.0 on TEST")

Bring up the context menu of this item by right-clicking on the item. Select the **Undeploy** option from the context menu. Deployit will generate a steplist that is needed to undeploy all application components from the infrastructure:

![Undeployment - PetPortal 2.0 on TEST - steplist](images/undeployment-petportal-2.0-on-TEST-steplist.png "Undeployment - PetPortal 2.0 on TEST - steplist")

Click the **Undeploy** button to undeploy the application, then **close** to close the undeployment window itself.

You can try accessing the PetPortal URL or Release Dashboard to validate the undeployment.

# That's it! #

That's the end of the Deployit online demo script. Hopefully you've gotten a feel for Deployit's capabilities and ease of use.

We've only touched on the basics of what Deployit can do for you, so feel free to play around with the product in this environment. If you get stuck or are unsure what other features Deployit has, take a look at the [online documentation](http://docs.xebialabs.com).
