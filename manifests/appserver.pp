# Install JBoss

#file { "/download-cache/jboss-5.1.0.GA.zip":
#	ensure   => file,
#	source   => "http://sourceforge.net/projects/jboss/files/JBoss/JBoss-5.1.0.GA/jboss-5.1.0.GA.zip/download",
#	require  => [File["/opt/deployit-puppet-module"]]
#}

exec { "extract-jboss-server":
        require => [Package['unzip'],Package['openjdk-6-jdk']],
	cwd => "/opt",
	command => "/usr/bin/unzip -o /download-cache/jboss-5.1.0.GA.zip -d /opt",
	creates => "/opt/jboss-5.1.0.GA",
}
