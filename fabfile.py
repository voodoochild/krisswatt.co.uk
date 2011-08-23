import os
from fabric.api import env, require, run, cd, hide, settings as fabric_settings

env.project = 'krisswatt.co.uk'
env.repository = 'git://github.com/voodoochild/krisswatt.co.uk.git'

def mythlan():
    """Production server."""
    env.hosts = ['mythlan.co.uk']
    env.user = 'kw'
    env.path = '/home/kw/%(project)s' % env
    env.default_branch = 'master'

def branch(branch):
    """Specify a branch."""
    env.branch = branch

def _require_server():
    """Require that a server definition is specified."""
    require('hosts', provided_by=[mythlan], used_for="working out which server to connect to.")

def _require_branch():
    """Require that a branch is specified."""
    if 'branch' not in env and env.default_branch is not False:
        env.branch = env.default_branch
    require('branch', provided_by=[mythlan])

def setup():
    """Clone a new version of the project to the specified path."""
    clone_project()
    deploy()

def deploy():
    """Deploy to an existing checkout."""
    checkout()

def clone_project():
    """Clone the project to env.path."""
    _require_server()
    run('git clone %(repository)s %(path)s' % env)

def checkout():
    """Checkout from the specified branch."""
    _require_server()
    _require_branch()
    with cd(env.path):
        run('git fetch origin')
        with fabric_settings(hide('warnings'), warn_only=True):
            run('git checkout -b %(branch)s origin/%(branch)s' % env)
        run('git checkout %(branch)s' % env)
        run('git pull origin %(branch)s' % env)
