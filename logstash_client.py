from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.context_managers import cd
import pwd
import os
from fabric.contrib.files import append

env.sudo_user = "ubuntu"
env.user = "ubuntu"
env.use_ssh_config = True


def get_uptime():
    run("uptime")


#Run this command with ex:"fab -f nagios_client.py test --hosts=apl-cluster-host-1"
@task
def test():
    get_uptime()


def install_java():
    run('sudo apt-get install -y openjdk-7-jdk')


def create_logstash_dirs():
    run('sudo mkdir /opt/logstash')
    run('sudo mkdir /var/log/logstash')
    run('sudo mkdir /etc/logstash')


def download_logstash():
    with cd('/opt/logstash'):
        run('sudo wget https://download.elasticsearch.org/logstash/logstash/logstash-1.4.1.tar.gz')


def extract_logstash():
    with cd('/opt/logstash'):
        run('sudo tar -xvzf logstash-1.4.1.tar.gz')


def put_logstash_config():
    put('server.conf', '/var/tmp', use_sudo=True)


def put_logstash_init():
    put('logstash.conf', '/var/tmp', use_sudo=True)


def mv_logstash_config():
    run('sudo mv /var/tmp/server.conf /etc/logstash/')


def mv_logstash_init():
    run('sudo mv /var/tmp/logstash.conf /etc/init')


def create_logstash_user():
    run('sudo useradd -g adm logstash')


def start_logstash():
    run('sudo service logstash start')


@task
def deploy():
    #install_java()
    create_logstash_dirs()
    download_logstash()
    extract_logstash()
    put_logstash_config()
    create_logstash_user()
    put_logstash_init()
    mv_logstash_init()
    mv_logstash_config()
    start_logstash()