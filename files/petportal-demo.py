from com.xebialabs.deployit.core.api.dto import ConfigurationItemDtos

def create(id, type, values):
   return factory.configurationItem(id, type, values)

def verifyNoValidationErrors(entity):
   if entity.validations is None or len(entity.validations) == 0:
       return entity
   else:
       raise Exception("Validations are present! Id=%s, Error:\n " % (entity.id, entity.validations.toString()))

def verifyNoValidationErrorsInRepoObjectsEntity(repositoryObjects):
   for repoObject in repositoryObjects.objects:
       verifyNoValidationErrors(repoObject)

def saveRepositoryObjectsEntity(repoObjects):
	print "Saving repository objects"
	repositoryObjects = repository.create(repoObjects)
	verifyNoValidationErrorsInRepoObjectsEntity(repositoryObjects)
	print "Saved repository objects"
	return repositoryObjects

def save(listOfCis):
	ros=ConfigurationItemDtos()
	ros.objects=listOfCis
	return saveRepositoryObjectsEntity(ros)

def resolveInfraId(id):
	id = id if id.startswith("Infrastructure/") else "Infrastructure/%s" % id
	return id;
	
def createLocalHost(id):
	return create(resolveInfraId(id),'overthere.LocalHost',{'os':'UNIX','temporaryDirectoryPath':'/tmp'})

def createVagrantSshHost(id, ipAddress):
	return create(resolveInfraId(id),'overthere.SshHost',{'address':ipAddress,'os':'UNIX','connectionType':'SUDO','username':'vagrant','password':'vagrant','port':'22', 'sudoUsername':'root', 'temporaryDirectoryPath':'/tmp'})

def createLocalHostAndDummyApacheServer(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'www.ApacheHttpdServer', {'host': hostId,'stopCommand':'echo stopping','startWaitTime':'0','startCommand':'echo starting','stopWaitTime':'0','defaultDocumentRoot':'/tmp','configurationFragmentDirectory':'/tmp'}))

def createLocalHostAndDummyJBossServer(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'jbossas.ServerV5', {'host': hostId, 'home':'/tmp', 'serverName':'default', 'controlPort':'1099','httpPort':'8080','ajpPort':'8009'}))

def createLocalHostAndDummyOracleClient(hostId,serverNames, infraList, createHost=True):
	hostId = (resolveInfraId(hostId))
	if createHost:
		infraList.append(createLocalHost(hostId))
	for serverName in serverNames:
		serverId = "%s/%s" % (hostId,serverName)
		infraList.append(create(serverId,'sql.OracleClient', {'host': hostId, 'oraHome':'/tmp', 'sid':'default'}))

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
repository.create(factory.configurationItem('Infrastructure/Ops/South','core.Directory',{}))

repository.create(factory.configurationItem('Environments/Dev','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops/Acc','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Ops/Prod','core.Directory',{}))
repository.create(factory.configurationItem('Environments/Dictionaries','core.Directory',{}))

infrastructureList = []

# Acceptation Environment Infrastructure
createLocalHostAndDummyApacheServer('Ops/North/ACC-Webserver-1', ['Apache-1'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/ACC-Webserver-2', ['Apache-2'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/North/ACC-Appserver-1',['AppServer-1'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/ACC-Appserver-2',['AppServer-2'], infrastructureList)
createLocalHostAndDummyOracleClient('Ops/North/ACC-Database-1',['ACC-Oracle-1'], infrastructureList)
createLocalHostAndDummyOracleClient('Ops/South/ACC-Database-2',['ACC-Oracle-2'], infrastructureList)

# Developement Environment Infrastructure
createLocalHostAndDummyApacheServer('Dev/DEV-Localhost', ['DEV-Apache'], infrastructureList)
createLocalHostAndDummyJBossServer('Dev/DEV-Localhost',['DEV-AppServer'], infrastructureList, False)
createLocalHostAndDummyOracleClient('Dev/DEV-Localhost',['DEV-MySql'], infrastructureList, False)
infrastructureList.append(create('Infrastructure/Dev/DEV-Localhost/DEV-TestRunner','tests2.TestRunner',{'host':'Infrastructure/Dev/DEV-Localhost','name':'TEST-TestRunner'}))

# Real Vagrant Test Environment Infrastructure
webServerHost = createVagrantSshHost('Infrastructure/Dev/TEST-Webserver','192.168.1.11')
infrastructureList.append(webServerHost)
infrastructureList.append(create('Infrastructure/Dev/TEST-Webserver/TEST-Apache','www.ApacheHttpdServer', {'host': webServerHost.id,'stopCommand':'/usr/sbin/apache2ctl stop','startWaitTime':'5','startCommand':'/usr/sbin/apache2ctl start','stopWaitTime':'0','defaultDocumentRoot':'/var/www','configurationFragmentDirectory':'/etc/apache2/conf.d'}))
infrastructureList.append(create('Infrastructure/Dev/TEST-Webserver/TEST-TestRunner','tests2.TestRunner',{'host':webServerHost.id,'name':'TEST-TestRunner'}))

appServerHost = createVagrantSshHost('Infrastructure/Dev/TEST-Appserver','192.168.1.12')
infrastructureList.append(appServerHost)
infrastructureList.append(create('Infrastructure/Dev/TEST-Appserver/TEST-AppServer','jbossas.ServerV5',{'home':'/opt/jboss-5.1.0.GA','host':appServerHost.id,'controlPort':'1099','httpPort':'8080','ajpPort':'8009','serverName':'default'}))

dbServerHost = createVagrantSshHost('Infrastructure/Dev/TEST-Database','192.168.1.13')
infrastructureList.append(dbServerHost)
infrastructureList.append(create('Infrastructure/Dev/TEST-Database/TEST-MySql','sql.MySqlClient',{'host':dbServerHost.id,'password':'{b64}vNteSNQBPd8QU4OwGM6Yfw==','databaseName':'petportal','username':'petportal','mySqlHome':'/usr'}))


# Production Environment Infrastructure
createLocalHostAndDummyApacheServer('Ops/North/PROD-Webserver-1', ['Apache-1'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/PROD-Webserver-2', ['Apache-2'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/North/PROD-Webserver-3', ['Apache-3'], infrastructureList)
createLocalHostAndDummyApacheServer('Ops/South/PROD-Webserver-4', ['Apache-4'], infrastructureList)

createLocalHostAndDummyJBossServer('Ops/North/PROD-Appserver-1',['PROD-AppServer-1'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/PROD-Appserver-2',['PROD-AppServer-2'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/North/PROD-Appserver-3',['PROD-AppServer-3'], infrastructureList)
createLocalHostAndDummyJBossServer('Ops/South/PROD-Appserver-4',['PROD-AppServer-4'], infrastructureList)

createLocalHostAndDummyOracleClient('Ops/North/PROD-Database-1',['PROD-Oracle-1'], infrastructureList)
createLocalHostAndDummyOracleClient('Ops/South/PROD-Database-2',['PROD-Oracle-2'], infrastructureList)
createLocalHostAndDummyOracleClient('Ops/North/PROD-Database-3',['PROD-Oracle-3'], infrastructureList)
createLocalHostAndDummyOracleClient('Ops/South/PROD-Database-4',['PROD-Oracle-4'], infrastructureList)
save(infrastructureList)


environmentsList = []

environmentsList.append(create('Environments/Dev/TEST','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict'], 'members':['Infrastructure/Dev/TEST-Webserver/TEST-TestRunner', 'Infrastructure/Dev/TEST-Webserver/TEST-Apache','Infrastructure/Dev/TEST-Database/TEST-MySql', 'Infrastructure/Dev/TEST-Appserver/TEST-AppServer']}))
environmentsList.append(create('Environments/Ops/Acc/ACC','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict'], 'members':['Infrastructure/Ops/South/ACC-Database-2/ACC-Oracle-2','Infrastructure/Ops/North/ACC-Database-1/ACC-Oracle-1','Infrastructure/Ops/South/ACC-Webserver-2/Apache-2','Infrastructure/Ops/North/ACC-Webserver-1/Apache-1','Infrastructure/Ops/South/ACC-Appserver-2/AppServer-2','Infrastructure/Ops/North/ACC-Appserver-1/AppServer-1']}))
environmentsList.append(create('Environments/Dev/DEV','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict-DEV'], 'members':['Infrastructure/Dev/DEV-Localhost/DEV-TestRunner','Infrastructure/Dev/DEV-Localhost/DEV-Apache', 'Infrastructure/Dev/DEV-Localhost/DEV-MySql', 'Infrastructure/Dev/DEV-Localhost/DEV-AppServer']}))
environmentsList.append(create('Environments/Ops/Prod/PROD','udm.Environment',{'dictionaries': ['Environments/Dictionaries/PetPortal-Dict'],
  'members':['Infrastructure/Ops/South/PROD-Database-2/PROD-Oracle-2','Infrastructure/Ops/North/PROD-Database-1/PROD-Oracle-1','Infrastructure/Ops/South/PROD-Webserver-2/Apache-2','Infrastructure/Ops/North/PROD-Webserver-1/Apache-1',
    'Infrastructure/Ops/South/PROD-Database-4/PROD-Oracle-4','Infrastructure/Ops/North/PROD-Database-3/PROD-Oracle-3','Infrastructure/Ops/South/PROD-Webserver-4/Apache-4','Infrastructure/Ops/North/PROD-Webserver-3/Apache-3',
    'Infrastructure/Ops/North/PROD-Appserver-1/PROD-AppServer-1','Infrastructure/Ops/North/PROD-Appserver-3/PROD-AppServer-3','Infrastructure/Ops/South/PROD-Appserver-2/PROD-AppServer-2','Infrastructure/Ops/South/PROD-Appserver-4/PROD-AppServer-4']}))


environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict','udm.Dictionary',
  {'entries':{'APACHE_PORT':'8000','APACHE_HOST':'192.168.1.11','APPSERVER_HOST':'192.168.1.12','APPSERVER_PORT':'8080',
  'DB_URL':'jdbc:oracle:thin:@192.168.1.13:orcl', 'PETPORTAL_TITLE':'Dierenportaal','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclinic'}}))
environmentsList.append(create('Environments/Dictionaries/PetPortal-Dict-DEV','udm.Dictionary',
  {'entries':{'APACHE_PORT':'80','APACHE_HOST':'localhost','APPSERVER_HOST':'localhost','APPSERVER_PORT':'80',
  'DB_URL':'jdbc:oracle:thin:@localhost:orcl', 'PETPORTAL_TITLE':'Dierenportaal','DB_USERNAME':'petportal','DB_PASSWORD':'petportal','PETCLINIC_CONTEXT_ROOT':'petclini'}}))
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
app = repository.read('Applications/PetPortal')
app.deploymentPipeline = [ 'Environments/Dev/DEV','Environments/Dev/TEST','Environments/Ops/Acc/ACC','Environments/Ops/Prod/PROD' ]
repository.update(app)

app = repository.read('Applications/PetClinic-war')
app.deploymentPipeline = [ 'Environments/Dev/DEV','Environments/Dev/TEST','Environments/Ops/Acc/ACC','Environments/Ops/Prod/PROD' ]
repository.update(app)

app = repository.read('Applications/PetClinic-ear')
app.deploymentPipeline = [ 'Environments/Dev/DEV','Environments/Dev/TEST','Environments/Ops/Acc/ACC','Environments/Ops/Prod/PROD' ]
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



