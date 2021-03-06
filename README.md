# GFE's Membership System

Gaming For Everyone is an intersectional feminist gaming association. We publish a list of servers that follow our social rules.
This is the system that handles the social part of our sites, the membership and server list system.

It currently holds basic support for
- Forums under server heading, and under categories.
- Registration in a Sverok-friendly format.
- A very basic volunteer system where people can apply to become admins on servers.

## Project status:

Very much alpha stage. Everything is in flux, and not completly smoothly integrated.
But, we have a 'Release early, release often' mindset, and transparency (all our code is open source, and also all our content go under a creative commons license as a rule of thumb), 
and we are excited to show you the general direction of where we are heading.


## To setup:

This is the entire list of install instructions for Debian linux, from a truly clean install to installed and working.

###1. First we install the basic requirements:

```
apt-get update
apt-get dist-upgrade
apt-get install git python-pip apache2 mysql-server libmysqlclient-dev python-dev phpmyadmin libapache2-mod-wsgi libpng-dev libjpeg-dev
```

We use mysql as a standard, though nothing in the code requires it at the moment. It does come with a really nice web gui, phpmyadmin, which is why we use it in our examples

###2. Next, we create a user:

```
adduser django
su - django
```

First command adds the user, the second command lets you take control of it.

###3. Download the sources..

```
git clone --recursive https://github.com/magnusjjj/gfesys.git
cd gfesys
```

The first command downloads the sources. The second jumps into the directory created.

IMPORTANT: Notice the --recursive in the command! Its very important, and without it you won't download the whole of the system and will get all kinds of strange errors.

###4. Setup the database:

- Go to http://your_ip_adress/phpmyadmin
- Log in
- Go in under privileges
- 'Add new user'
- Choose a username, password, and let host be empty. Check the box that says  'Create a database with the same name and grant all privileges'
- Press 'create user'
- At the bottom of the page there is now a link 'reload privileges'. Press it.

###4. Run the installer:

```
./installer.py
```

###5. Run the server :)

```
./manage.py runserver 0.0.0.0:8000
```

This starts a webserver at port 8000 for simple testing.

###(optional) 6. Configure apache. You can see a horribly bad example below, which goes in your web server config.

```
nano /etc/apache2/sites-enabled/000-default
```

plonk in:

```ApacheConf
Alias /static/ /home/django/gfe/static/
Alias /media/ /home/django/gfe/media/

<Directory /home/django/gfe/static>
	Order allow,deny
	Allow from all

	Require all granted
	Satisfy Any
</Directory>

<Directory /home/django/gfe/media>
	Order allow,deny
	Allow from all

	Require all granted
	Satisfy Any
</Directory>


WSGIScriptAlias / /home/django/gfe/gfe/wsgi.py
WSGIPythonPath /home/django/gfe/
<Directory /home/django/gfe/gfe/>
        <Files wsgi.py>
			Order allow,deny
			Allow from all

			Require all granted
			Satisfy Any
        </Files>
</Directory>
```
