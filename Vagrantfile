# -*- mode: ruby -*-
# vi: set ft=ruby :
BOX = "archlinux/archlinux"
HOSTNAME = "vmbox" 
IP_ADDRESS = "192.168.1.20" 
CPUS = 2
MEMORY = 512
MAC_ADDRESS = "080027123456"
IFACE = "enp3s0"
DOMAIN_NAME = "#{HOSTNAME}.lan"


Vagrant.configure("2") do |config|
  config.vm.define HOSTNAME do |host|
    host.vm.box = BOX
    host.vm.hostname = HOSTNAME
    host.vm.network "public_network",
      bridge: IFACE,
      ip: IP_ADDRESS,
      mac: MAC_ADDRESS

    host.vm.provider :virtualbox do |vbox|
      vbox.cpus = CPUS
      vbox.memory = MEMORY
    end
    config.vm.provision "shell", path: "script.sh", args: [DOMAIN_NAME]
  end
end

