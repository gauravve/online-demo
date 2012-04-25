# Puppet demo manifest

class httpd {
  
  #
  # Yum update
  #
  exec { "yum-update":
    command     => "/usr/bin/yum update",
  }

  Exec["yum-update"] -> Package <| |>

  package { 'httpd':
    ensure => present,
  }

  service { 'httpd':
    ensure => running,
  }
}
include httpd
