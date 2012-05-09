#
# Yum update
#
exec { "apt-get-update":
  command     => "/usr/bin/apt-get update",
}

Exec["apt-get-update"] -> Package <| |>

import "appserver.pp"
import "database.pp"
import "webserver.pp"
import "deployit.pp"

