
########
# Global constants for the test data: 

DEPLOYMENT_USERNAME = "deployment"
DEPLOYMENT_PASSWORD = "deployment"
APACHE_HOST = "localhost"
JBOSS_HOST = "localhost"
MYSQL_HOST = "localhost"
DEPLOYIT_HOST = "localhost"

def create(id, type, values):
   return factory.configurationItem(id, type, values)

def verifyNoValidationErrors(entity):
   if entity.validations is None or len(entity.validations) == 0:
       return entity
   else:
       raise Exception("Validations are present! Id=%s, Error:\n " % (entity.id, entity.validations.toString()))

def verifyNoValidationErrorsInRepoObjectsEntity(repositoryObjects):
   for repoObject in repositoryObjects:
       verifyNoValidationErrors(repoObject)

def saveRepositoryObjectsEntity(repoObjects):
	print "Saving repository objects"
	repositoryObjects = repository.create(repoObjects)
	verifyNoValidationErrorsInRepoObjectsEntity(repositoryObjects)
	print "Saved repository objects"
	return repositoryObjects

def save(listOfCis):
	return saveRepositoryObjectsEntity(listOfCis)

def resolveInfraId(id):
	id = id if id.startswith("Infrastructure/") else "Infrastructure/%s" % id
	return id;
	
def createLocalHost(id):
	return create(resolveInfraId(id),'overthere.LocalHost',{'os':'UNIX','temporaryDirectoryPath':'/tmp'})

def createVagrantSshHost(id, ipAddress):
	return create(resolveInfraId(id),'overthere.SshHost',{'address':ipAddress,'os':'UNIX','connectionType':'INTERACTIVE_SUDO','username':DEPLOYMENT_USERNAME,'password':DEPLOYMENT_PASSWORD,'port':'22', 'sudoUsername':'root', 'temporaryDirectoryPath':'/tmp'})

def createLocalHostAndDummyApacheServer(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'demo.ApacheHttpdServer', {'host': hostId,'stopCommand':'echo stopping','startWaitTime':'0','startCommand':'echo starting','stopWaitTime':'0','defaultDocumentRoot':'/tmp','configurationFragmentDirectory':'/tmp','deploymentGroup':hostId[-1]}))

def createLocalHostAndDummyJBossServer(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'demo.JBoss', {'host': hostId, 'home':'/tmp', 'serverName':'default', 'controlPort':'1099','httpPort':'8080','ajpPort':'8009','deploymentGroup':hostId[-1]}))

def createLocalHostAndDummyMySqlClient(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'demo.MySql', {'host': hostId, 'password':'{b64}vNteSNQBPd8QU4OwGM6Yfw==','databaseName':'petportal','username':'petportal','mySqlHome':'/tmp','deploymentGroup':hostId[-1]}))

def deleteIds(ids):
	for id in ids:
		repository.delete(id)

def deployAndSkipSteps(app, env):
  newDep = deployment.prepareInitial(app,env)
  newDep = deployment.generateAllDeployeds(newDep)
  taskInfo = deployment.deploy(newDep)
  stepsToSkip = range(1,len(taskInfo.steps)+1)
  deployit.skipSteps(taskInfo.id, stepsToSkip)
  deployit.startTaskAndWait(taskInfo.id)
  print "Deployment of %s to %s finished with state %s" % (app, env, deployit.retrieveTaskInfo(taskInfo.id).state)		


#clean up
deleteIds(['Applications/Composite', 'Applications/PetPortal', 'Applications/PetClinic-war', 'Applications/PetClinic-ear', 'Environments/Dev', 'Environments/Ops', 'Environments/Dictionaries', 'Infrastructure/Dev','Infrastructure/Ops'])

# Create directories
repository.create(factory.configurationItem('Infrastructure/Dev','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/North','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/North/Acc','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/North/Prod','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/South','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/South/Acc','core.Directory',{}))
repository.create(factory.configurationItem('Infrastructure/Ops/South/Prod','core.Directory',{}))

repository.create(factory.configurationItem('Environments/Dev','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops/Acc','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops/Prod','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Dictionaries','core.Directory',{}))

infrastructureList = []

# Acceptation Environment Infrastructure
createLocalHostAndDummyApacheServer('Ops/North/Acc/Webserver-1', ['Apache'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/Acc/Webserver-2', ['Apache'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/North/Acc/Appserver-1',['JBoss'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/Acc/Appserver-2',['JBoss'], infrastructureList)
createLocalHostAndDummyMySqlClient('Ops/North/Acc/Database-1',['MySql'], infrastructureList)
createLocalHostAndDummyMySqlClient('Ops/South/Acc/Database-2',['MySql'], infrastructureList)

# Developement Environment Infrastructure
createLocalHostAndDummyApacheServer('Dev/DevServer-1', ['Apache'], infrastructureList)
createLocalHostAndDummyJBossServer('Dev/DevServer-1',['JBoss'], infrastructureList, False)
createLocalHostAndDummyMySqlClient('Dev/DevServer-1',['MySql'], infrastructureList, False)

# Real Vagrant Test Environment Infrastructure
webServerHost = createVagrantSshHost('Infrastructure/Dev/Webserver-1', APACHE_HOST)
infrastructureList.append(webServerHost)
infrastructureList.append(create('Infrastructure/Dev/Webserver-1/Apache','www.ApacheHttpdServer', {'host': webServerHost.id,'stopCommand':'/usr/sbin/apachectl stop','startWaitTime':'5','startCommand':'/usr/sbin/apachectl start','stopWaitTime':'0','defaultDocumentRoot':'/var/www','configurationFragmentDirectory':'/etc/httpd/conf.d','restartCommand':'/usr/sbin/apachectl restart', 'restartWaitTime':'0'}))
infrastructureList.append(create('Infrastructure/Dev/Webserver-1/TestRunner','tests2.TestRunner',{'host':webServerHost.id,'name':'TestRunner'}))

appServerHost = createVagrantSshHost('Infrastructure/Dev/Appserver-1',JBOSS_HOST)
infrastructureList.append(appServerHost)
infrastructureList.append(create('Infrastructure/Dev/Appserver-1/JBoss','jbossas.ServerV5',{'home':'/opt/jboss-5.1.0.GA','host':appServerHost.id,'controlPort':'1099','httpPort':'8080','ajpPort':'8009','serverName':'default','startWaitTime':'45'}))

dbServerHost = createVagrantSshHost('Infrastructure/Dev/Database-1',MYSQL_HOST)
infrastructureList.append(dbServerHost)
infrastructureList.append(create('Infrastructure/Dev/Database-1/MySql','sql.MySqlClient',{'host':dbServerHost.id,'password':'{b64}vNteSNQBPd8QU4OwGM6Yfw==','databaseName':'petportal','username':'petportal','mySqlHome':'/usr'}))


# Production Environment Infrastructure
createLocalHostAndDummyApacheServer('Ops/North/Prod/Webserver-1', ['Apache'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/Prod/Webserver-2', ['Apache'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/North/Prod/Webserver-3', ['Apache'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/Prod/Webserver-4', ['Apache'], infrastructureList)

createLocalHostAndDummyJBossServer('Ops/North/Prod/Appserver-1',['JBoss'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/Prod/Appserver-2',['JBoss'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/North/Prod/Appserver-3',['JBoss'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/Prod/Appserver-4',['JBoss'], infrastructureList)

createLocalHostAndDummyMySqlClient('Ops/North/Prod/Database-1',['MySql'], infrastructureList)
createLocalHostAndDummyMySqlClient('Ops/South/Prod/Database-2',['MySql'], infrastructureList)
createLocalHostAndDummyMySqlClient('Ops/North/Prod/Database-3',['MySql'], infrastructureList)
createLocalHostAndDummyMySqlClient('Ops/South/Prod/Database-4',['MySql'], infrastructureList)
save(infrastructureList)


environmentsList = []

environmentsList.append(create('Environments/Dev/DEV','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict-DEV'], 
	'members':[
		'Infrastructure/Dev/DevServer-1/Apache', 'Infrastructure/Dev/DevServer-1/MySql', 'Infrastructure/Dev/DevServer-1/JBoss'
		]}))
environmentsList.append(create('Environments/Dev/TEST','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict-TEST'], 
	'members':[
		'Infrastructure/Dev/Webserver-1/TestRunner', 'Infrastructure/Dev/Webserver-1/Apache','Infrastructure/Dev/Database-1/MySql', 'Infrastructure/Dev/Appserver-1/JBoss'
	]}))
environmentsList.append(create('Environments/Ops/Acc/ACC','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict-ACC'], 
	'members':[
		'Infrastructure/Ops/South/Acc/Database-2/MySql','Infrastructure/Ops/North/Acc/Database-1/MySql','Infrastructure/Ops/South/Acc/Webserver-2/Apache',
		'Infrastructure/Ops/North/Acc/Webserver-1/Apache','Infrastructure/Ops/South/Acc/Appserver-2/JBoss','Infrastructure/Ops/North/Acc/Appserver-1/JBoss'
	]}))
environmentsList.append(create('Environments/Ops/Prod/PROD','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict-PROD'],
  'members':[
  	'Infrastructure/Ops/South/Prod/Database-2/MySql','Infrastructure/Ops/North/Prod/Database-1/MySql','Infrastructure/Ops/South/Prod/Webserver-2/Apache',
  	'Infrastructure/Ops/North/Prod/Webserver-1/Apache','Infrastructure/Ops/South/Prod/Database-4/MySql','Infrastructure/Ops/North/Prod/Database-3/MySql',
  	'Infrastructure/Ops/South/Prod/Webserver-4/Apache','Infrastructure/Ops/North/Prod/Webserver-3/Apache','Infrastructure/Ops/North/Prod/Appserver-1/JBoss',
  	'Infrastructure/Ops/North/Prod/Appserver-3/JBoss','Infrastructure/Ops/South/Prod/Appserver-2/JBoss','Infrastructure/Ops/South/Prod/Appserver-4/JBoss'
   ]}))

environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict-DEV','udm.Dictionary',
  {'entries':{'APACHE_PORT':'800','APACHE_HOST':'localhost','APPSERVER_HOST':'localhost','APPSERVER_PORT':'8080',
  'DB_URL':'jdbc:mysql:@localhost:mysql', 'PETPORTAL_TITLE':'The Pet Portal (C) Site','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclinic'}}))
environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict-TEST','udm.Dictionary',
  {'entries':{'APACHE_PORT':'8000','APACHE_HOST':'localhost','APPSERVER_HOST':'localhost','APPSERVER_PORT':'8080',
  'DB_URL':'jdbc:mysql:@localhost:mysql', 'PETPORTAL_TITLE':'Pet Portal on TEST','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclinic'}}))
environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict-ACC','udm.Dictionary',
  {'entries':{'APACHE_PORT':'900','APACHE_HOST':'localhost','APPSERVER_HOST':'localhost','APPSERVER_PORT':'8080',
  'DB_URL':'jdbc:mysql:@localhost:mysql', 'PETPORTAL_TITLE':'Pet Portal on ACC','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclinic'}}))
environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict-PROD','udm.Dictionary',
  {'entries':{'APACHE_PORT':'9000','APACHE_HOST':'localhost','APPSERVER_HOST':'localhost','APPSERVER_PORT':'8080',
  'DB_URL':'jdbc:mysql:@localhost:mysql', 'PETPORTAL_TITLE':'Pet Portal on PROD','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclinic'}}))

save(environmentsList)

## Additional info for Security and Pipeline demo

# Import apps
deployit.importPackage('PetPortal/1.0')
deployit.importPackage('PetPortal/2.0')
deployit.importPackage('PetClinic-war/1.0')
deployit.importPackage('PetClinic-war/2.0')
deployit.importPackage('PetClinic-ear/1.0')
deployit.importPackage('PetClinic-ear/2.0')

# Create composite app
app = repository.create(factory.configurationItem('Applications/Composite', 'udm.Application'))
compPkg = repository.create(factory.configurationItem('Applications/Composite/1.0', 'udm.CompositePackage'))
compPkg.packages = ['Applications/PetPortal/1.0', 'Applications/PetClinic-war/1.0', 'Applications/PetClinic-ear/1.0']
repository.update(compPkg)
compPkg = repository.create(factory.configurationItem('Applications/Composite/2.0', 'udm.CompositePackage'))
compPkg.packages = ['Applications/PetPortal/2.0', 'Applications/PetClinic-war/2.0', 'Applications/PetClinic-ear/2.0']
repository.update(compPkg)

# Release overview: define deployment pipeline
pipeline = repository.create(factory.configurationItem('Configuration/Pipeline', 'release.DeploymentPipeline',{"pipeline":[ 'Environments/Dev/DEV','Environments/Dev/TEST','Environments/Ops/Acc/ACC','Environments/Ops/Prod/PROD' ]}))
app = repository.read('Applications/PetPortal')
app.pipeline = pipeline.id
repository.update(app)

app = repository.read('Applications/PetClinic-war')
app.pipeline = pipeline.id
repository.update(app)

app = repository.read('Applications/PetClinic-ear')
app.pipeline = pipeline.id
repository.update(app)

# Release overview: define environment conditions

env = repository.read('Environments/Dev/TEST')
env.requiresReleaseNotes = 'true'
repository.update(env)

env = repository.read('Environments/Ops/Acc/ACC')
env.requiresReleaseNotes = 'true'
env.requiresPerformanceTested = 'true'
repository.update(env)

env = repository.read('Environments/Ops/Prod/PROD')
env.requiresReleaseNotes = 'true'
env.requiresPerformanceTested = 'true'
env.requiresChangeTicketNumber = 'true'
repository.update(env)

#Do some deployments to the pipelines
def satisfiesReleaseNotes(app):
	app = repository.read(app)
	app.satisfiesReleaseNotes = 'true'
	repository.update(app)
	
def satisfiesPerformanceTested(app):
	app = repository.read(app)
	app.satisfiesPerformanceTested = 'true'
	repository.update(app)

satisfiesReleaseNotes('Applications/PetPortal/1.0')	
satisfiesPerformanceTested('Applications/PetPortal/1.0')
satisfiesReleaseNotes('Applications/PetPortal/2.0')	
deployAndSkipSteps('Applications/PetPortal/1.0', 'Environments/Dev/DEV')

satisfiesReleaseNotes('Applications/PetClinic-ear/1.0')
satisfiesPerformanceTested('Applications/PetClinic-ear/1.0')
satisfiesReleaseNotes('Applications/PetClinic-ear/2.0')
deployAndSkipSteps('Applications/PetClinic-ear/2.0', 'Environments/Dev/DEV')
deployAndSkipSteps('Applications/PetClinic-ear/2.0', 'Environments/Dev/TEST')
deployAndSkipSteps('Applications/PetClinic-ear/1.0', 'Environments/Ops/Acc/ACC')

satisfiesReleaseNotes('Applications/PetClinic-war/1.0')
deployAndSkipSteps('Applications/PetClinic-war/2.0', 'Environments/Dev/DEV')
deployAndSkipSteps('Applications/PetClinic-war/1.0', 'Environments/Dev/TEST')

# Create some security test data
security.createUser('developer', 'developer')
security.assignRole('developers', ['developer'])
security.createUser('deployer', 'deployer')
security.assignRole('deployers', ['deployer', 'sr-deployer'])
security.createUser('sr-deployer', 'sr-deployer')
security.assignRole('sr-deployers', ['sr-deployer'])
security.createUser('ops-north', 'ops-north')
security.assignRole('ops-north', ['ops-north'])
security.createUser('ops-south', 'ops-south')
security.assignRole('ops-south', ['ops-south'])
security.createUser('administrator', 'administrator')
security.assignRole('administrators', ['admin','administrator'])

# Grants
security.grant('login', 'developers')
security.grant('login', 'deployers')
security.grant('login', 'sr-deployers')
security.grant('login', 'ops-north')
security.grant('login', 'ops-south')
security.grant('login', 'administrators')

security.grant('import#upgrade', 'developers', [ 'Applications' ])
security.grant('deploy#upgrade', 'developers', [ 'Environments/Dev' ])

security.grant('import#initial', 'deployers', [ 'Applications' ])
security.grant('import#upgrade', 'deployers', [ 'Applications' ])
security.grant('deploy#initial', 'deployers', [ 'Environments/Ops/Acc', 'Environments/Dev' ])
security.grant('deploy#upgrade', 'deployers', [ 'Environments/Ops/Acc', 'Environments/Dev' ])
security.grant('read', 'deployers', [ 'Environments/Ops' ])
security.grant('read', 'deployers', [ 'Environments/Dictionaries' ])
security.grant('repo#edit', 'deployers', [ 'Environments/Dictionaries' ])

security.grant('import#initial', 'sr-deployers', [ 'Applications' ])
security.grant('import#upgrade', 'sr-deployers', [ 'Applications' ])
security.grant('deploy#initial', 'sr-deployers', [ 'Environments/Ops/Prod' ])
security.grant('deploy#upgrade', 'sr-deployers', [ 'Environments/Ops/Prod' ])
security.grant('read', 'sr-deployers', [ 'Environments/Ops' ])

security.grant('repo#edit', 'ops-north', [ 'Infrastructure/Ops/North' ])
security.grant('read', 'ops-north', [ 'Infrastructure/Ops', 'Infrastructure/Ops/North' ])
security.grant('repo#edit', 'ops-south', [ 'Infrastructure/Ops/South' ])
security.grant('read', 'ops-south', [ 'Infrastructure/Ops', 'Infrastructure/Ops/South' ])
