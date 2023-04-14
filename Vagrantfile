# -*- mode: ruby -*-
# vi: set ft=ruby :
BOX = "archlinux/archlinux"
HOSTNAME = "vmbox" 
IP_ADDRESS = "192.168.1.20" 
CPUS = 2
MEMORY = 512
MAC = "080027123456"
IFACE = "enp5s0"
DOMAIN_NAME = "#{HOSTNAME}.lan"


Vagrant.configure("2") do |config|
  config.vm.define HOSTNAME do |box|
    box.vm.provider :virtualbox do |vbox, override|
      config.vm.box = BOX
      override.vm.hostname = HOSTNAME
      override.vm.network "public_network", 
        bridge: IFACE,
        ip: IP_ADDRESS, 
        mac: MAC
      vbox.cpus = CPUS 
      vbox.memory = MEMORY
    end
    config.vm.provision "shell", path: "script.sh", args: [DOMAIN_NAME]
  end
end

