from __future__ import with_statement

import os, re, sys
from datetime import datetime

from fabric import api
from fabric import operations

extra_index_url = 'http://webiken.net:9090/packages'

deploy_user = 'django'

deploy_dir = '/opt/django/bvd'

proj_dir = '%s/current/srv/bvd' % deploy_dir

host = 'webiken.net'

git_clone = 'git clone https://github.com/webiken/bvd.git'

collect_static = '%s/manage.py collectstatic --noinput' % proj_dir

syncdb = '%s/manage.py sync_db --noinput' % proj_dir

api.env.hosts = [host]
api.env.user = deploy_user

home_dir = os.environ.get('HOME')

virtualenv_dir = '%s/.virtualenvs/bvd' % home_dir
	

def deploy(*args,**kwargs):
	
	args = dict([(k,True) for k in args] + kwargs.items())

	home_dir = api.run('echo $HOME')

	virtualenv_dir = '%s/.virtualenvs/bvd' % home_dir

	with api.cd('%s' % deploy_dir):
		now = datetime.now()
		year = now.year
		dt = now.strftime('%Y-%m-%d_%H:%M:%S')

		mkdir = 'mkdir -p %s/%s' % (deploy_dir,year)

		api.run(mkdir)
		clone = '%s %s' % (git_clone,dt)

		with api.cd('%s' % year):
			api.run(clone)
		
		rm = 'rm -rf %(root)s/current'
		link = 'ln -nsf %(root)s/%(year)s/%(dt)s %(root)s/current' % dict(
			root = deploy_dir,
			year = year,
			dt = dt
		)

		api.run(link)

		settings_ln = 'ln -s %(home_dir)s/settings/bvd/settings.py %(root)s/current/src/bvd/settings.py' % dict(
				home_dir = home_dir,
				root = deploy_dir,
			)

		api.run(settings_ln)


	with api.cd('%s/current' % deploy_dir):
		install_requirements(remote=True)

	api.run(syncdb)
	api.run(collectstatic)

	if args.get('restart'):
		operations.sudo('service apache2 restart', user='admin')
		
def pypi_mirror_args(args):
	pypi_mirror = args.get('extra-index-url',None)
	if not pypi_mirror:
		return extra_index_url
	return pypi_mirror
		

def install_requirements(*args,**kwargs):
	args = dict([(k,True) for k in args] + kwargs.items())

	remote = args.get('remote',False)

	install = '%s/bin/pip install -r requirements.txt' % (virtualenv_dir)

	if remote:
		home_dir = api.run('echo $HOME')
		virtualenv_dir = '%s/.virtualenvs/bvd' % home_dir
		api.run('%(install)s' % dict(install=install))
	else:
		home_dir = os.environ.get('HOME')
		virtualenv_dir = '%s/.virtualenvs/bvd' % home_dir
		api.local('%(install)s' % dict(install = install))
