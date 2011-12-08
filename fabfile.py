import os
import site

from fabric.api import env, lcd, local, settings  # cd, sudo, run,
from fabric.colors import red as _red, green as _green, cyan as _cyan
from fabric.contrib.console import confirm

from fab_helpers import ve_local as _ve_local  # ve_run as _ve_run

# allow to look for modules in directory above
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)
site.addsitedir(path('../'))

# load fab_settings_local.py which is not shared
try:
    import fab_settings_local as sett
except ImportError:
    print _red("\r\nFabric is using default settings!\r\n")
    try:
        import fab_settings as sett
    except:
        print "Bazinga! no fab_settings.py or an error in import"
        raise


def commands(dev_type=None):
    "List of available commands"
    print _green("\n%s fabric script." % sett.PROJECT_NAME)
    print """
Usage: fab [localhost|stage|prod] (ve:virtualenv) command

To use another virtualenv as the standard one use the ve switch
fab localhost ve:myvirtualenv command

fab commands:dev    : List development commands
fab commands:deploy : List deployment commands
"""
    if not dev_type or dev_type == 'dev':
        print _green("Development commands")
        print """
install_dev - installs all dependencies needed for project to run and test
update_dev  - update all dependencies
commit      - commit current changes in the project and apps if PROJECT_DEV
runserver   - runse development server
syncdb      - synchronises database and migrates
check       - run check.py on all possible Python files
"""


def _setenv(server):
    env.hosts = [sett.SERVERS[server]]
    env.directory = sett.LOCAL_DIR[server]
    env.virtualenv = sett.VIRTUALENV[server]
    env.ve_wrapper = sett.VE_WRAPPER[server]
    env.workondir = sett.WORKON_HOME[server]
    env.branch = sett.BRANCH[server]
    env.main_dir = sett.MAIN_DIR[server]


def _default(server):
    if not hasattr(env, 'workondir'):
        _setenv(server)


def localhost():
    """run command on localhost"""
    _setenv('local')


def stage():
    """run command on localhost"""
    _setenv('stage')


def ve(virtualenv):
    """Temporary switch virtual environment
    """
    env.virtualenv = virtualenv


ALLAPS_PLUS = '+'.join(sett.ALLAPPS)
def test(apps=ALLAPS_PLUS, params=None):
    """Run unittests

    :param: apps (string) optional - apps which needs to be tested
            (separated by +), default ALLAPS_PLUS
    :param: params (string) optional - parameters of the ``./manage.py test``
            (separated by +), default coverage settings
    """
    _default('local')
    apps = apps.replace('+', ' ')
    # use all for apps to allow additional settings
    if apps == 'all':
        apps = sett.ALLAPS
    temp_cover_packages = apps.split(' ')
    cover_packages = []
    for cp in temp_cover_packages:
        cover_packages.append(cp.split('.')[0])
    cover_packages = ','.join(cover_packages)
    params = params.split('+') if params else []
    params.extend(['nocapture', 'nologcapture',
        #'with-fixture-bundling',
        'with-progressive',
        'with-coverage', 'cover-inclusive', 'cover-erase', 'cover-tests',
        'cover-exclude-module=base64,migrations,settings$',
        'cover-package=%s' % cover_packages])
    command = './manage.py test %s --%s' % (
            apps,
            ' --'.join(params))
    _ve_local(command)


def push(repo='origin', branch=None):
    """Push all commits to ``repo`` using branch ``branch``
    """
    _default('local')
    with lcd(env.directory):
        test()
        if not branch:
            # discover current branch
            branch = 'master'
        local('git status')
        if confirm("Should I push to repository %s banch %s?" %
                (repo, branch)):
            local('git push %s %s' % (repo, branch))
        if sett.PROJECT_TYPE == sett.PROJECT_DEV:
            for app in sett.APPS:
                print _cyan("\nPushing to %s" % app)
                with lcd(os.path.join(
                        env.workondir, env.virtualenv, 'src', app)):
                    local("git status")
                    if confirm(("Should I checkout and push to "
                        "repository %s banch %s?") %
                            (repo, branch)):
                        local("git checkout %s" % branch)
                        local('git push %s %s' % (repo, branch))


def status(*args):
    _default('local')
    apps = args or sett.APPS
    local('git status')
    if sett.PROJECT_TYPE == sett.PROJECT_DEV:
        for app in apps:
            print _cyan("\n%s" % app)
            with lcd(os.path.join(
                    env.workondir, env.virtualenv, 'src', app)):
                local("git status")


def check(command=None, *args):
    """Run check.py on all Python files in all dev apps
    """
    _default('local')
    apps = args or sett.APPS
    if command:
        return _ve_local("check.py %s" % command)
    command = ["check.py *py apps/*py utils/*py apps/*/*py apps/*/tests/*py"]
    if sett.PROJECT_TYPE == sett.PROJECT_DEV:
        for app in apps:
            directory = os.path.join(
                    env.workondir, env.virtualenv, 'src', app, app)
            command.append("%s/*py" % directory)
            if os.path.isdir("%s/tests" % directory):
                command.append("%s/tests/*py" % directory)
    _ve_local(' '.join(command))


def commit(*args):
    """Commit changes from working project, (and all other apps if PROJECT_DEV)
    """
    _default('local')
    apps = args or sett.APPS
    with settings(warn_only=True):
        local("git status")
        result = local("git add -p && git commit -v")
        if (result.failed
                and sett.PROJECT_TYPE == sett.PROJECT_DEV
                and not confirm('Proceed further?')):
            return
        if sett.PROJECT_TYPE == sett.PROJECT_DEV:
            for app in apps:
                print _cyan("\n******* Commit (%s) *******" % app)
                with lcd(os.path.join(
                        env.workondir, env.virtualenv, 'src', app)):
                    local("git status")
                    result = local("git add -p && git commit -v ")
                if (result.failed and sett.APPS[-1] != app
                        and not confirm('Proceed further?')):
                    return


def runserver(port=8000):
    """Runs the development server

    :param: port (int) on which port should the runserver be run

    Example: fab runserver
             fab runserver:8091
    """
    _default('local')
    _ve_local('./manage.py runserver %d' % int(port))


def prepare_deploy():
    _default('local')
    test()
    commit()


def deploy():
    # pull system
    # create virtual env
    # pip install requirements
    # test?
    pass


def update_dev(repository='upstream'):
    """Update development packages

    Depending on PROJECT_TYPE it runs pip updates dev3rdparty or edge
    If PROJECT_DeV it also git checkes master and pulls master from upstream

    Example: fab update_dev
    """
    _default('local')
    if not os.path.exists(env.workondir):
        if not confirm("No virtualenv provided. Should I install?"):
            return
        install_dev()
        return
    local("git status")
    if confirm("Should I checkout to and pull from master?"):
        local("git checkout master && git pull %s master" % repository)

    if sett.PROJECT_TYPE == sett.PROJECT_DEV:
        # update APPS
        _ve_local("pip install -r requirements/dev3rdparty.pip")
        for app in sett.APPS:
            with lcd(os.path.join(env.workondir, env.virtualenv, 'src', app)):
                print _cyan('Updating %s' % app)
                local("git status")
                if confirm("Should I checkout to and pull from master"):
                    local("git status")
                    local("git checkout master && git pull %s master" % repository)
    if sett.PROJECT_TYPE == sett.PROJECT_EDGE:
        # update APPS from master branch
        _ve_local("pip install -r requirements/edge.pip --upgrade")


def dev_from_edge():
    """move APPS to MAIN_DIR and link them in virtual environment

    Example: fab dev_from_edge
    """
    _default('local')
    if not sett.GIT_ORIGIN:
        print "Configure GIT_ORIGIN (git@github.com:{your username})"
        return False
    for app in sett.APPS:
        if not os.path.isdir(os.path.join(env.main_dir, app)):
            local("mv %s %s" % (
                os.path.join(env.workondir, env.virtualenv, 'src', app),
                os.path.join(env.main_dir, app)))
            local("ln -fs %s %s" % (
                os.path.join(env.main_dir, app),
                os.path.join(env.workondir, env.virtualenv, 'src', app)))
            with lcd(os.path.join(env.main_dir, app)):
                local("git remote rm origin")
                local("git remote add origin %s/jsfiddle-%s.git" %
                        (sett.GIT_ORIGIN, app))
                local(("git remote add upstream "
                    "git@github.com:jsfiddle/jsfiddle-%s.git") % app)
    return True


def install_dev():
    """Install dev environment and dependencies

    Installs pip, virtualenv and virtualenvwrapper
    Creates workon directory
    Updates all (eventual) submodules
    Installs simplejson, mysql-python and edge dependencies
    If PROJECT_DEV dev_from_edge is called

    Example: fab install_dev
    """
    _default('local')
    local('sudo easy_install pip')
    local('sudo pip install virtualenvwrapper')
    local('sudo pip install virtualenv')
    if not os.path.exists(env.workondir):
        local("mkdir %s" % env.workondir)
    if not os.path.exists(os.path.join(env.workondir, env.virtualenv)):
        # Create virtual environment
        local("""
            export WORKON_HOME=%s &&
            source %s &&
            mkvirtualenv --no-site-packages %s
            """ % (env.workondir, env.ve_wrapper, env.virtualenv))
    local("git submodule update --init --recursive")
    _ve_local("""
             pip install simplejson &&
             pip install mysql-python &&
             pip install -r requirements/edge.pip""")
    if sett.PROJECT_TYPE == sett.PROJECT_DEV:
        if not dev_from_edge():
            return
    test()


def update_requirements(require='dev3rdparty'):
    """Runs pip install -r requirements on the right file
    """
    _default('local')
    _ve_local("pip install -r requirements/compiled.pip")
    _ve_local("pip install -r requirements/%s.pip" % require)
    test()


def createsuperuser():
    """Creates django project admin

    Example: fab createsuperuser
    """
    _default('local')
    _ve_local('./manage.py createsuperuser')


def syncdb():
    """Synchronise db and runs migrate

    Example: fab syncdb
    """
    _default('local')
    _ve_local("./manage.py syncdb")
    _ve_local("./manage.py migrate")


def reset_migrations():
    """Remove migrations in all apps and create new ones
    """
    if sett.PROJECT_TYPE == sett.PROJECT_DEV:
        _default('local')
        local('rm -rf apps/*/migrations')
        for app in sett.APPS:
            with lcd(os.path.join(
                    env.workondir, env.virtualenv, 'src', app, app)):
                local('rm -rf migrations')
        _ve_local('./manage.py reset south')
        for app in sett.ALLAPPS:
            print _green('converting %s to south' % app)
            _ve_local('./manage.py convert_to_south %s' % app)
        migrate()


def makedocs(target='html'):
    """Compile development docs

    Example: fab makedocs:pdf
    """
    _default('local')
    with lcd(os.path.join(env.directory, 'docs')):
        _ve_local('make %s' % target)


def manage(*args):
    """Run ./manage.py commands

    Example: fab manage:south
    """
    _default('local')
    _ve_local('./manage.py %s' % ' '.join(args))


def schemamigration(app, sattr='--auto', mattr=None):
    """Change the database for the given app

    :param: app (string) which app was changed
    :param: sattr (string) schemamigration additional attributes,
            defaults to "auto". other useful setting is ``--initial``
    :param: mattr (string) migrate additional attributes, defaults to None.

    Example: fab schema:appname
    Example: fab schema:appname,--initial
    Example: fab schema:appname,001+--fake
    """
    _default('local')
    sattr = ' '.join(sattr.split('+'))
    _ve_local('./manage.py schemamigration %s %s' % (app, sattr))
    mcommand = './manage.py migrate %s' % app
    if mattr:
        mattr = ' '.join(mattr.split('+'))
        mcommand += ' %s' % mattr
    _ve_local(mcommand)


def migrate(app=None, attr=None):
    """Migrate database

    :param: app (string) limit migration to this app only
    """
    _default('local')
    app = app or ''
    command = './manage.py migrate %s' % app
    if attr:
        attr = ' '.join(attr.split('+'))
        command += ' %s' % attr
    _ve_local(command)


def harvest(apps=None):
    """Harvest thelettuce behaviour tests

    :param: apps (plus separated string) apps which should be harvested

    Example: fab harvest
             fab harvest:fiddle
    """
    _default('local')
    command = "./manage.py harvest"
    if apps:
        apps = apps.replace('+', ',')
        command += " --apps=%s" % apps
    _ve_local(command)
