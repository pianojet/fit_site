# -*- mode: ruby -*-
# vi: set ft=ruby :

##
## Utilize vagrant 1.1+
#
# echo "10.44.4.10  dev.justinerictaylor.com" >> /etc/hosts
# echo "10.44.4.10  servicedev.justinerictaylor.com" >> /etc/hosts
# # Check out https://github.com/mosaicxm/vagrant-hostmaster
#
$mysql_password = ENV["MYSQL_PASSWORD"] || "bankon17"


# Just a little initial setup for convenience w/ bootstrap, etc.
$environment_script = <<SCRIPT
cd /vagrant
rm -rf venv
./bootstrap.py venv
source venv/bin/activate

pip install -r requirements.debug.txt

ln -fs /vagrant/backend/apache/vhost.vagrant.servicedev.conf /etc/apache2/sites-available/servicedev.conf
ln -fs /vagrant/frontend/apache/vhost.vagrant.dev.conf /etc/apache2/sites-available/dev.conf
a2dissite 000-default
a2ensite servicedev.conf
a2ensite dev.conf

mkdir -p /var/log/fit
touch /var/log/fit/fit_debug.log

grep -q "FIT" ~/.bashrc
if [ $? -eq 1 ]; then
  echo -e "\n# FIT environment" >> /home/vagrant/.bashrc
  echo -e "export DJANGO_SETTINGS_MODULE=fit.settings.dev" >> /home/vagrant/.bashrc
  echo -e "source /vagrant/venv/bin/activate" >> /home/vagrant/.bashrc
  echo -e "cd /vagrant" >> /home/vagrant/.bashrc 
fi
SCRIPT

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "trusty64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"


  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 80, host: 47080, auto_correct: true
  config.vm.network :forwarded_port, guest: 8000, host: 47800, auto_correct: true
  #config.vm.network :forwarded_port, guest: 3306, host: 47306, auto_correct: true
  #config.vm.network :forwarded_port, guest: 27017, host: 47017, auto_correct: true

  config.ssh.forward_agent = true

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "10.44.4.10"
  config.vm.host_name = "dev.justinerictaylor.com"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider :virtualbox do |vb|
    # Don't boot with headless mode
    # vb.gui = true
 
    # Use VBoxManage to customize the VM. For example to change memory:
    # vb.customize ["modifyvm", :id, "--memory", "1024"]
    # Make the guest use the host for name resolution, so names on the VPN will
    # work.
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end
  
  # View the documentation for the provider you're using for more
  # information on available options.
  if Vagrant.has_plugin?("vagrant-cachier")
    # Configure cached packages to be shared between instances of the same base box.
    # More info on the "Usage" link above
    config.cache.scope = :box

    # OPTIONAL: If you are using VirtualBox, you might want to use that to enable
    # NFS for shared folders. This is also very useful for vagrant-libvirt if you
    # want bi-directional sync
    config.cache.synced_folder_opts = {
      type: :nfs,
      # The nolock option can be useful for an NFSv3 client that wants to avoid the
      # NLM sideband protocol. Without this option, apt-get might hang if it tries
      # to lock files needed for /var/cache/* operations. All of this can be avoided
      # by using NFSv4 everywhere. Please note that the tcp option is not the default.
      mount_options: ['rw', 'vers=3', 'tcp', 'nolock']
    }
  end

  config.vm.provision :shell, 
    :inline => "debconf-set-selections <<< 'msql-server-5.5 mysql-server/root_password password #{$mysql_password}' && " +
    "debconf-set-selections <<< 'msql-server-5.5 mysql-server/root_password_again password #{$mysql_password}'"

  config.vm.provision :shell, 
    :inline => "apt-get update -qq && " +
               "apt-get -q -y install " +
               "apache2 openssh-server apache2-mpm-worker libapache2-mod-wsgi python-pip git mysql-client " + 
               "libmysqlclient-dev python2.7-dev python2.7 build-essential pkg-config " +
               "sensible-mda mysql-server vim"
  
  config.vm.provision :shell, 
    :inline => 'grep -q default-storage-engine /etc/mysql/my.cnf || sed -i -e "/\[mysqld\]/a default-storage-engine=myisam" /etc/mysql/my.cnf'

  config.vm.provision :shell, 
    :inline => "echo 'create database if not exists fit;' | mysql -uroot -p#{$mysql_password}"

  config.vm.provision :shell, :inline => $environment_script
end

