# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.define :deployit do |deployit_config|
    deployit_config.vm.box = "precise32"
    #deployit_config.vm.forward_port(4516, 4516)
    #deployit_config.vm.forward_port(80, 8000)
    #deployit_config.vm.share_folder("vagrant-dropbox", "/dropbox", "../vagrant/shared/folders/dropbox")
    deployit_config.vm.customize ["modifyvm", :id, "--memory", 2048]
    deployit_config.vm.customize ["modifyvm", :id, "--name", "deployit-online-demo"]
    deployit_config.vm.share_folder("download-cache", "/download-cache", "../catalog/OnlineDemo")
    deployit_config.vm.share_folder("catalog", "/catalog", ENV["CATALOG"])
    deployit_config.vm.share_folder("demo-files", "/demo-files", "./files")
    deployit_config.vm.network(:hostonly, "192.168.0.10")

    # Enable the Puppet provisioner
    deployit_config.vm.provision :puppet do |puppet|
      puppet.options = "--verbose --debug"
      puppet.manifest_file = "singlevm.pp"
      puppet.manifests_path = "manifests"
      puppet.module_path = [ "modules" ]
    end
  end
end
