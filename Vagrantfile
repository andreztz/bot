# -*- mode: ruby -*-
# vi: set ft=ruby :
BOX = "archlinux/archlinux"
HOSTANAME = "vmbox" 
IP = "192.168.1.20" 
CPUS = 2
MEMORY = 512
MAC = "080027123456"
IFACE = "enp5s0"
DOMAIN = HOSTANAME + ".lan"


Vagrant.configure("2") do |config|
  config.vm.define HOSTANAME do |box|
    box.vm.provider :virtualbox do |vbox, override|
      config.vm.box = BOX
      override.vm.hostname = HOSTANAME
      override.vm.network "public_network", 
        bridge: IFACE,
        ip: IP, 
        mac: MAC
      vbox.cpus = CPUS 
      vbox.memory = MEMORY
    end
    config.vm.provision "shell", path: "script.sh", args: [DOMAIN]
  end
end

