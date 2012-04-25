# Database

$mysql_password = 'centos'

#
# Yum update
#
exec { "yum-update":
    command     => "/usr/bin/yum update",
}

Exec["yum-update"] -> Package <| |>

  package { "mysql-server": ensure => installed }
  package { "mysql-client": ensure => installed }

  service { "mysql":
    enable => true,
    ensure => running,
    require => Package["mysql-server"],
  }

  exec { "set-mysql-password":
    unless => "mysqladmin -uroot -p$mysql_password status",
    path => ["/bin", "/usr/bin"],
    command => "mysqladmin -uroot password $mysql_password",
    require => Service["mysql"],
  }

 exec { "create-petportal-db":
      unless => "/usr/bin/mysql -upetportal -ppetportal petportal",
      command => "/usr/bin/mysql -uroot -p$mysql_password -e \"create database petportal; grant all on petportal.* to petportal@localhost identified by 'petportal';\"",
      require => Exec["set-mysql-password"],
 }
