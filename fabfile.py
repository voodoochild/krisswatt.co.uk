import os
from fabric.api import env, require, run, cd, hide, settings as fabric_settings

env.project = 'krisswatt.co.uk'
env.repository = 'git://github.com/voodoochild/krisswatt.co.uk.git'

def mythlan():
    env.hosts = ['mythlan.co.uk']
    env.user = 'kw'
    env.path = '/home/kw/%(project)s' % env
    env.default_branch = 'master'

def branch(branch):
    env.branch = branch
    return True

def _require_server():
    require('hosts', provided_by=[mythlan], used_for="working out which server to connect to.")
    return True

def _require_branch():
    if 'branch' not in env and env.default_branch is not False:
        env.branch = env.default_branch
    require('branch', provided_by=[mythlan])
    return True

def setup():
    """
    Clone a new version of the project to the specified path.
    """
    clone_project()
    deploy()
    return True

def deploy():
    """
    Deploy to an existing checkout.
    """
    checkout()
    return True

def clone_project():
    _require_server()
    run('git clone %(repository)s %(path)s' % env)
    return True

def checkout():
    _require_server()
    _require_branch()
    with cd(env.path):
        run('git fetch origin')
        with fabric_settings(hide('warnings'), warn_only=True):
            run('git checkout -b %(branch)s origin/%(branch)s' % env)
        run('git checkout %(branch)s' % env)
        run('git pull origin %(branch)s' % env)
    return True
