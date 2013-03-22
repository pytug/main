## set up django on ubuntu 12.10, assuming a clean installation
## most of it is sourced from http://www.lennu.net/2012/05/14/django-deployement-installation-to-ubuntu-12-dot-04-server/
## some commands are using relative paths, i.e. it is imoprtant that they are executed in the order that they are given.

## define variables suiting your environment
HOSTNAME=pytug
DOMAIN=$HOSTNAME.com
DB_NAME=pytugdb
DB_USER=pytuger
DB_PASSWORD=examplepassword
WSGI_USER=pywsgi

# get latest updates (i.e. update the list of package repositories and get the actual updates)
apt-get update
apt-get upgrade

# edit your servername, defined above
echo "$HOSTNAME" > /etc/hostname
hostname -F /etc/hostname
echo -e "\n127.0.0.1 $HOSTNAME.local $HOSTNAME.com $HOSTNAME \n" >> /etc/hosts

# install some packages and dependancies (apache, python, virtualenv, pip)
apt-get -y install apache2-mpm-worker apache2-threaded-dev
apt-get -y install python python-dev python-setuptools
easy_install virtualenv virtualenvwrapper pip

# install and enable wsgi module for apache, disable the default apache site
apt-get install libapache2-mod-wsgi
a2enmod wsgi
a2dissite default

# install and configure mysql, variables are defined above
apt-get -y install mysql-server mysql-client
echo "CREATE DATABASE $DB_NAME;" | mysql -u root -p
echo "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$PASSWORD';" | mysql -u root -p
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';" | mysql -u root -p
echo "FLUSH PRIVILEGES;" | mysql -u root -p

# install python environment and django
cd /srv/
mkdir -p my_project/app my_project/app/conf/apache
mkdir -p my_project/logs my_project/run/eggs
virtualenv my_project/venv
/srv/my_project/venv/bin/pip install django

# django is installed now, start a django project
pushd my_project/app/
/srv/my_project/venv/bin/python /srv/my_project/venv/bin/django-admin.py startproject webapp
popd

# create some folders, and a wsgi file
mkdir -p my_project/app/webapp/site_media
mkdir -p my_project/app/templates
cd my_project/app/conf/apache/

# create a django.wsgi file with the following contents
# (just copy-paste the following block of commands into the terminal
cat >> django.wsgi << EOF
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'venv/lib/python2.7/site-packages/')))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'app')))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'app', 'webapp')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
EOF

# create a system user to run wsgi, i called mine simply- $WSGI_USER
useradd --system --no-create-home --home-dir /srv/my_project/ --user-group $WSGI_USER
chsh -s /bin/bash $WSGI_USER

# now, create an apache config file for the domain
# and paste the following configuration (inside hashes), no need to paste the hashes
cat >> /etc/apache2/sites-available/$DOMAIN << EOF
<VirtualHost *:80>
ServerAdmin root@$DOMAIN
ServerName $DOMAIN

Alias /site_media/ /srv/my_project/app/webapp/site_media/
Alias /static/ /srv/my_project/venv/lib/python2.7/site-packages/django/contrib/admin/static/
Alias /robots.txt /srv/my_project/app/webapp/site_media/robots.txt
Alias /favicon.ico /srv/my_project/app/webapp/site_media/favicon.ico

CustomLog "|/usr/sbin/rotatelogs /srv/my_project/logs/access.log.%Y%m%d-%H%M%S 5M" combined
ErrorLog "|/usr/sbin/rotatelogs /srv/my_project/logs/error.log.%Y%m%d-%H%M%S 5M"
LogLevel warn

WSGIDaemonProcess $DOMAIN user=$WSGI_USER group=$WSGI_USER processes=1 threads=15 maximum-requests=10000 python-path=/srv/my_project/venv/lib/python2.7/site-packages python-eggs=/srv/my_project/run/eggs
WSGIProcessGroup $DOMAIN
WSGIScriptAlias / /srv/my_project/app/conf/apache/django.wsgi

<Directory /srv/my_project/app/webapp/site_media>
Order deny,allow
Allow from all
Options -Indexes FollowSymLinks
</Directory>

<Directory /srv/my_project/app/conf/apache>
Order deny,allow
Allow from all
</Directory>

</VirtualHost>
EOF

# enable the newly created configuration for the site
a2ensite $DOMAIN


# install mysql module for python
apt-get build-dep python-mysqldb
/srv/my_project/venv/bin/pip install MySQL-python

# set permissions to the project to our created system user and restart apache
chown -R $WSGI_USER:$WSGI_USER /srv/my_project/
service apache2 restart

#### MANUALLY #############
## configure django with our / your paths, open the setting.py with nano editor, and..
#cd ../../
#cd webapp/webapp/
#nano settings.py
#
## ..and find the following directives (MEDIA_ROOT and TEMPLATE_DIRS) and ammend these lines to look like this
#MEDIA_ROOT = '/srv/my_project/app/webapp/site_media/'
#TEMPLATE_DIRS = '/srv/my_project/app/templates/',
############################


# check if it worked, e.g. with firefox $DOMAIN

## YOU SHOULD GET A PAGE that says that it worked, congrats with on your first django-powered site, well, congrats!!

## TODO
## more useful things to do
