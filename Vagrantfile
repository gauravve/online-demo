# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.define :deployit do |deployit_config|
    deployit_config.vm.box = "deployit-linux-base"
    deployit_config.vm.forward_port(4516, 4516)
    deployit_config.vm.share_folder("vagrant-dropbox", "/dropbox", "../vagrant/shared/folders/dropbox")
    deployit_config.vm.share_folder("download-cache", "/download-cache", "../vagrant/shared/folders/download-cache")
    deployit_config.vm.share_folder("demo-files", "/demo-files", "./files")
    deployit_config.vm.network(:hostonly, "192.168.1.10")

    # Enable the Puppet provisioner
    deployit_config.vm.provision :puppet do |puppet|
      puppet.manifest_file = "deployit.pp"
      puppet.manifests_path = "manifests"
      puppet.module_path = "../vagrant/shared/puppet"
    end
  end
end
