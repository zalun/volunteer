CMS Core - Django boilerplate
=============================

This is a base for future CMS projects.

The goal is to create a system which will run many CMS sites from one
main directory with this Django project

Currently based only on django-fiber

Install
-------

.. code-block:: python

   mkvirtualenv cms-core --no-site-packages
   workon cms-core
   git clone git://github.com/zalun/cms-core.git
   cd cms-core
   pip install -r requirements/compiled.rst
   pip install -r requirements/production.pip
   mkdir -w media/uploads
   # create local config (especially database access)
   vi settings_local.py
   # create database
   ./manage.py syncdb
   ./manage.py migrate)

License
-------
Mozilla Public License
