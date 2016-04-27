# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 5432, host: 5432

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib

    echo "host all all all password" >> /etc/postgresql/*/main/pg_hba.conf
    echo "listen_addresses = '*'" >> /etc/postgresql/*/main/postgresql.conf
    service postgresql restart

    sudo -u postgres psql -c "CREATE USER weiqi WITH PASSWORD '6ff6zzHxLmuLMpyuRyMC';"
    sudo -u postgres psql -c "CREATE DATABASE weiqi OWNER weiqi;"
    sudo -u postgres psql -c "CREATE DATABASE weiqi_test OWNER weiqi;"
  SHELL
end
