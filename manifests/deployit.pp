# Puppet demo manifest

# Ensure Deployit is downloaded & installed

$DEPLOYIT_VERSION = '3.7.1'
$JBOSSAS_PLUGIN_VERSION = '3.7.0'
$WLS_PLUGIN_VERSION = '3.7.0'

class { 'deployit':
  cliHome => '/home/ec2-user/deployit-cli',
}

class deployit-install {

  deployit::server { 'install-server':
    serverArchive => "/download-cache/deployit-${DEPLOYIT_VERSION}-server.zip",
    ensure => present,
  }

  deployit::cli { 'install-cli':
    destinationDir => '/home/ec2-user',
    cliArchive => "/download-cache/deployit-${DEPLOYIT_VERSION}-cli.zip",
    ensure => present,
  }

  # Install jbossas-plugin

  file { 'install-jbossas-plugin':
    path => "/opt/deployit-server/plugins/jbossas-plugin-${JBOSSAS_PLUGIN_VERSION}.jar",
    source   => "/download-cache/jbossas-plugin-${JBOSSAS_PLUGIN_VERSION}.jar",
    ensure => "present",
    require => Deployit::Server["install-server"],
  }

  file { 'install-wls-plugin':
    path => "/opt/deployit-server/plugins/wls-plugin-${WLS_PLUGIN_VERSION}.jar",
    source   => "/download-cache/wls-plugin-${WLS_PLUGIN_VERSION}.jar",
    ensure => "present",
    require => Deployit::Server["install-server"],
  }

  file { 'install-http-tester':
    path => "/opt/deployit-server/plugins/deployment-test2-plugin-1.0-milestone-7.jar",
    source   => "/download-cache/deployment-test2-plugin-1.0-milestone-7.jar",
    ensure => "present",
    require => Deployit::Server["install-server"],
  }

  file { 'install-petportal':
    path => "/opt/deployit-server/importablePackages/PetPortal",
    source   => "/demo-files/PetPortal",
    ensure => directory,
    recurse => true,
    require => Deployit::Server["install-server"],
  }

  # Install support for Apache ProxyPass settings

  file { 'install-synthetic':
    path => "/opt/deployit-server/ext/synthetic.xml",
    source   => "/demo-files/synthetic.xml",
    ensure => present,
    require => Deployit::Server["install-server"],
  }

  file { 'install-proxypass-template':
    path => "/opt/deployit-server/ext/www",
    source   => "/demo-files/www",
    ensure => directory,
    recurse => true,
    require => Deployit::Server["install-server"],
  }

  # Install fix for deployment-test2 plugin script

  file { 'install-deployment-test2-fix':
    path => "/opt/deployit-server/ext/tests2",
    source   => "/demo-files/tests2",
    ensure => present,
    recurse => true,
    require => Deployit::Server["install-server"],
  }
}

class deployit-start {
    deployit::server { 'start-server':
    ensure => running,
  }
}

class deployit-data {
  deployit::exec { 'load-data':
    source => '/demo-files/petportal-demo.py',
    require => Deployit::Server["start-server"],
  }  
}

include deployit-install
include deployit-start
include deployit-data

Class["deployit-install"] -> Class["deployit-start"] -> Class["deployit-data"]
