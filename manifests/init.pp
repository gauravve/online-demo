# Deployit online demo manifest

include deployit-install
include deployit-start
include deployit-data

Class["deployit-install"] -> Class["deployit-start"] -> Class["deployit-data"]
