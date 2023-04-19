sudo timedatectl set-timezone America/Sao_Paulo
# Archlinux
# sudo pacman -Sy --noconfirm
# sudo pacman -S python --noconfirm
# sudo pacman -S prosody --noconfirm
# sudo pacman -S luarocks --noconfirm
# sudo pacman -S gcc --noconfirm
# sudo pacman -S unbound --noconfirm
# sudo luarocks install luaunbound
# sudo systemctl start prosody.service

# Debian
sudo apt update -y
sudo apt install lua5.3 -y
sudo apt install luarocks -y
sudo apt install prosody -y
sudo apt install unbound -y

sudo usermod -aG prosody vagrant

sudo touch /run/prosody/prosody.pid
sudo chown prosody:prosody /run/prosody/prosody.pid
sudo cp /vagrant/prosody.cfg.lua /etc/prosody/prosody.cfg.lua

# sudo prosodyctl cert generate vmbox.lan
# Gera as chaves
openssl req -newkey rsa:2048 -nodes \
    -keyout /etc/prosody/certs/vmbox.lan.key \
    -out /etc/prosody/certs/vmbox.lan.csr \
    -subj "/CN=vmbox.lan"

openssl x509 -req -days 365 -in /etc/prosody/certs/vmbox.lan.csr \
    -signkey /etc/prosody/certs/vmbox.lan.key \
    -out /etc/prosody/certs/vmbox.lan.crt

sudo chown -R prosody:prosody /etc/prosody/certs/
# sudo usermod -a -G prosody prosody

sudo chmod 640 /etc/prosody/certs/vmbox.lan.key
sudo chown root:prosody /etc/prosody/certs/vmbox.lan.key 

# Tests
# [vagrant@vmbox prosody]$ sudo prosodyctl check certs
# Checking certificates...
# Checking certificate for vmbox.lan
#   Certificate: /etc/prosody/certs/vmbox.lan.crt
# All checks passed, congratulations!

# sudo -u prosody cat /path/to/certificate.key # Should succeed
# sudo -u nobody cat /path/to/certificate.key # Should fail

python3 /vagrant/init.py vmbox.lan

sudo systemctl restart prosody.service
