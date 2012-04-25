# Puppet demo manifest

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
