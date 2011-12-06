#!/usr/bin/env python
import os
import sys
import site

try:
    import env_local
except:
    pass

from django.core.management import execute_manager, setup_environ

import piston

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

prev_sys_path = list(sys.path)

site.addsitedir(path('apps'))
site.addsitedir(path('../'))

# Move the new items to the front of sys.path. (via virtualenv)
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

try:
    import settings_local as settings
except ImportError:
    try:
        import settings
    except ImportError:
        sys.stderr.write("Error: Can't find the file 'settings.py' in the "
                         "directory containing %r.\n(If the file settings.py"
                         " does indeed exist, it's causing an ImportError "
                         "somehow.)\n" % __file__)
        raise

setup_environ(settings)

if settings.PRODUCTION:
    # remove development apps
    for app in settings.DEV_APPS:
        if app in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.remove(app)
    # remove development middlewares
    for middleware in settings.DEV_MIDDLEWARE_CLASSES:
        if middleware in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES.remove(middleware)


if __name__ == "__main__":
    execute_manager(settings)
