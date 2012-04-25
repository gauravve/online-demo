# Puppet demo manifest

#
# Apt-get update
#
exec { "apt-update":
    command     => "/usr/bin/apt-get update",
}

Exec["apt-update"] -> Package <| |>

package { 'apache2':
  ensure => present,
}

service { 'apache2':
  ensure => running,
  require => File['/etc/apache2/mods-enabled/proxy.load'],
}

# Enable mod_proxy modules
file { '/etc/apache2/mods-enabled/proxy.load':
  target => "/etc/apache2/mods-available/proxy.load",
  ensure => link,
  require => Package["apache2"],
}

file { '/etc/apache2/mods-enabled/proxy_http.load':
  target => "/etc/apache2/mods-available/proxy_http.load",
  ensure => link,
  require => Package["apache2"],
}
