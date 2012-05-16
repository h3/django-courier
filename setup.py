# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-courier',
    version='0.0.3',
    description='Allows easy configuration of notifications and management of email templates. ',
    author='Maxime Haineault (Motion Média)',
    author_email='max@motion-m.ca',
    url='',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
#   package_data={'courier': [
#       'templates/*',
#       'static/*',
#   ]},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Motion Média :: Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)



