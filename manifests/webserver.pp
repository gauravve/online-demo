# Puppet demo manifest

class httpd {
  
  package { 'apache2':
    ensure => present,
  }

  service { 'apache2':
    ensure => running,
    require => Package["apache2"],
  }
}
include httpd
