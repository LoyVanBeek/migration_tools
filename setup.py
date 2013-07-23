#!/usr/bin/env python

from distutils.core import setup

setup(  name='migration_tools',
        version='0.1.0',
        author='Loy van Beek',
        author_email='loy.vanbeek@gmail.com',
        scripts=['migrate.py', 'clone_all.py'],
        url='http://github.com/tue-robotics-lab/migration_tools',
        license='LICENSE.txt',
        description='Useful towel-related stuff.',
        long_description=open('README.md').read(),
        install_requires=["sh", "PyGithub"]
)