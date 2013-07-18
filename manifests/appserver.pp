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

exec { "start-jboss-server":
        require => Exec['extract-jboss-server'],
	cwd => "/opt/jboss-5.1.0.GA/bin",
	command => "nohup /opt/jboss-5.1.0.GA/bin/run.sh -b 0.0.0.0 &",
}

