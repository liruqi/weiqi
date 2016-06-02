# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# NOTE:
# Vagrant is not required to run the weiqi.gs development environment.
# It only serves to test the PostgreSQL and RabbitMQ backends.

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.network "forwarded_port", guest: 5672, host: 5672
  config.vm.network :forwarded_port, guest: 15672, host: 15672

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
    wget -O- https://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add -

    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib rabbitmq-server

    rabbitmq-plugins enable rabbitmq_management
    echo '[{rabbit, [{loopback_users, []}]}].' > /etc/rabbitmq/rabbitmq.config
    /etc/init.d/rabbitmq-server restart

    echo "host all all all password" >> /etc/postgresql/*/main/pg_hba.conf
    echo "listen_addresses = '*'" >> /etc/postgresql/*/main/postgresql.conf
    service postgresql restart

    sudo -u postgres psql -c "CREATE USER weiqi WITH PASSWORD '6ff6zzHxLmuLMpyuRyMC';"
    sudo -u postgres psql -c "CREATE DATABASE weiqi OWNER weiqi;"
    sudo -u postgres psql -c "CREATE DATABASE weiqi_test OWNER weiqi;"
  SHELL
end
