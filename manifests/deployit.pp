# Puppet demo manifest

# Ensure Deployit is downloaded & installed

$DEPLOYIT_VERSION = '3.9.2'
$JBOSSAS_PLUGIN_VERSION = '3.8.1'
$WLS_PLUGIN_VERSION = '3.9.0'
$TESTER_PLUGIN_VERSION = '3.8.0'

$DEPLOYIT_SERVER_ARCHIVE = "/download-cache/deployit-${DEPLOYIT_VERSION}-server.zip"
$DEPLOYIT_CLI_ARCHIVE = "/download-cache/deployit-${DEPLOYIT_VERSION}-cli.zip"
$JBOSSAS_PLUGIN_ARCHIVE = "/download-cache/jbossas-plugin-${JBOSSAS_PLUGIN_VERSION}.jar"
$WLS_PLUGIN_ARCHIVE = "/download-cache/wls-plugin-${WLS_PLUGIN_VERSION}.jar"
$TESTER_PLUGIN_ARCHIVE = "/download-cache/deployment-test2-plugin-${TESTER_PLUGIN_VERSION}.jar"

# The following allows this Puppet file to be run on vagrant for local testing & EC2 in production
$CLI_HOME = $operatingsystem ? {
    'Ubuntu' => '/home/vagrant',
    default => '/home/ec2-user',
}

$HOMEPAGE_TEMPLATE = $operatingsystem ? {
    'Ubuntu' => '/vagrant/templates/homepage.erb',
    default => '/etc/puppet/online-demo/templates/homepage.erb',
}

Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class { 'deployit':
  cliHome => "${CLI_HOME}/deployit-cli",
}

class deployit-install {

  exec { 'download-deployit-server':
    unless => "test ! -e /usr/bin/s3get || test -e ${DEPLOYIT_SERVER_ARCHIVE}",
    command => "s3get deployit-online-demo/deployit-${DEPLOYIT_VERSION}-server.zip ${DEPLOYIT_SERVER_ARCHIVE}",
    #require => [Package['unzip'],Package['openjdk-6-jdk']]
  }

  deployit::server { 'install-server':
    serverArchive => "${DEPLOYIT_SERVER_ARCHIVE}",
    ensure => present,
    require => Exec["download-deployit-server"],
  }

  exec { 'download-deployit-cli':
    unless => "test ! -e /usr/bin/s3get || test -e ${DEPLOYIT_CLI_ARCHIVE}",
    command => "s3get deployit-online-demo/deployit-${DEPLOYIT_VERSION}-cli.zip ${DEPLOYIT_CLI_ARCHIVE}",
  }

  deployit::cli { 'install-cli':
    destinationDir => "${CLI_HOME}",
    cliArchive => "${DEPLOYIT_CLI_ARCHIVE}",
    ensure => present,
    require => Exec["download-deployit-cli"],
  }

  # Install jbossas-plugin

  exec { 'download-jbossas-plugin':
    unless => "test ! -e /usr/bin/s3get || test -e ${JBOSSAS_PLUGIN_ARCHIVE}",
    command => "s3get deployit-online-demo/jbossas-plugin-${JBOSSAS_PLUGIN_VERSION}.jar ${JBOSSAS_PLUGIN_ARCHIVE}",
  }

  file { 'install-jbossas-plugin':
    path => "/opt/deployit-server/plugins/jbossas-plugin-${JBOSSAS_PLUGIN_VERSION}.jar",
    source   => "${JBOSSAS_PLUGIN_ARCHIVE}",
    ensure => "present",
    require => [ Exec["download-jbossas-plugin"], Deployit::Server["install-server"] ],
  }

  # Install wls-plugin

  exec { 'download-wls-plugin':
    unless => "test ! -e /usr/bin/s3get || test -e ${WLS_PLUGIN_ARCHIVE}",
    command => "s3get deployit-online-demo/wls-plugin-${WLS_PLUGIN_VERSION}.jar ${WLS_PLUGIN_ARCHIVE}",
  }

  file { 'install-wls-plugin':
    path => "/opt/deployit-server/plugins/wls-plugin-${WLS_PLUGIN_VERSION}.jar",
    source   => "${WLS_PLUGIN_ARCHIVE}",
    ensure => "present",
    require => [ Exec["download-wls-plugin"], Deployit::Server["install-server"] ],
  }

  # Install http-tester

  exec { 'download-tester-plugin':
    unless => "test ! -e /usr/bin/s3get || test -e ${TESTER_PLUGIN_ARCHIVE}",
    command => "s3get deployit-online-demo/deployment-test2-plugin-${TESTER_PLUGIN_VERSION}.jar ${TESTER_PLUGIN_ARCHIVE}",
  }

  file { 'install-http-tester':
    path => "/opt/deployit-server/plugins/deployment-test2-plugin-${TESTER_PLUGIN_VERSION}.jar",
    source   => "${TESTER_PLUGIN_ARCHIVE}",
    ensure => "present",
    require => [ Exec["download-tester-plugin"], Deployit::Server["install-server"] ],
  }

  file { 'install-petportal':
    path => "/opt/deployit-server/importablePackages/PetPortal",
    source   => "/demo-files/PetPortal",
    ensure => directory,
    recurse => true,
    require => Deployit::Server["install-server"],
  }

  # Install custom synthetic

  file { 'install-synthetic':
    path => "/opt/deployit-server/ext/synthetic.xml",
    source   => "/demo-files/synthetic.xml",
    ensure => present,
    require => Deployit::Server["install-server"],
  }

  # Install support for Apache ProxyPass settings

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

  file { 'install-demo-plugin':
    path => "/opt/deployit-server/ext/demo",
    source   => "/demo-files/demo",
    ensure => directory,
    recurse => true,
    require => Deployit::Server["install-server"],
  }

  file { ['/tmp/server', '/tmp/server/default', '/tmp/server/default/deploy']:
    ensure => directory,
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

class online-demo-docs {
  # Install online demo docs

  file { ['/var', '/var/www']:
    #require => [Package['unzip'],Package['openjdk-6-jdk'],Package['curl']],
    ensure => directory,
  }

  file { 'install-online-demo-docs':
    path => "/var/www/html",
    source   => "/demo-files/html",
    ensure => present,
    recurse => true,
  }

  file { 'install-online-demo-homepage':
    path => "/var/www/html/index.markdown",
    content   => template("${HOMEPAGE_TEMPLATE}"),
    ensure => file,
    require => File['install-online-demo-docs'],
  }
}

class package_unzip {
        package { "unzip": ensure => "installed" }
}

class package_java {
	package { "openjdk-6-jdk": ensure => "installed" }
}

class package_curl {
	package { "curl": ensure => "installed" }
}

class package_libapache2-mod-proxy-html {
	package { "libapache2-mod-proxy-html": ensure => "installed" }
}

class enable_proxy_pass {
	exec { 'enable-proxy-pass-mod':
        cwd => '/etc/apache2/mods-enabled',
	command => '/bin/ln -s ../mods-available/proxy_http.load .;/bin/ln -s ../mods-available/proxy.load .;/bin/ln -s ../mods-available/headers.load .',
	#require => Package['libapache2-mod-proxy-html'],
    }
}

class file_rc_local {
    file { '/etc/rc.local':
       content =>
       "/usr/bin/nohup /opt/jboss-5.1.0.GA/bin/run.sh -b 0.0.0.0 &
	/usr/bin/nohup /opt/deployit-server/bin/server.sh &
       exit 0",
    ensure => present,
    mode => 755,
  }
}

class start_jboss {
  exec { "start-jboss-server":
        require => File['/etc/rc.local'],
        cwd => "/opt/jboss-5.1.0.GA/bin",
        command => "nohup /opt/jboss-5.1.0.GA/bin/run.sh -b 0.0.0.0 &",
  }
}


include file_rc_local
#include enable_proxy_pass
#include package_libapache2-mod-proxy-html
#include package_unzip
#include package_java
#include package_curl
include start_jboss
include deployit-install
include deployit-start
include deployit-data
include online-demo-docs

Class["online-demo-docs"] -> Class["deployit-install"] -> Class["deployit-start"] -> Class["deployit-data"]
