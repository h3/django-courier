django-courier
==============

Dead simple email notification system


Introduction
------------

Allows easy configuration of notifications and management of email templates.

* `Screenshots Screenshots <http://code.google.com/p/django-courier/wiki/Screenshots>`_


Project goals
-------------

* Allow administrators to setup email notifications on any models without programming knowledge
* Allow administrators to create and modify email templates easily
* Be as simple and unobtrusive as possible to setup


Similar projects
----------------

If this project does not fit your needs, you might want to look at `django-notification <https://github.com/jtauber/django-notification/>`_.

Key differences between django-courier and django-notification:

* No need to setup notifications from Python
* Email templates are stored in database
* Email templates are rendered using Django template system (with the sender object as context)
* Everything is manageable from the admin interface
* Transparent integration with `django-modeltranslation <http://code.google.com/p/django-modeltranslation/>`_


Known issues
------------

* If you set an EmailNotification on the User model on create and modified signal, you will get a created AND a modified notification upon User creation. This is related to the way the User model are created (I guess).
* Compatible with only with Django >= 1.3


Credits
=======

This project was created and is sponsored by:

.. figure:: http://motion-m.ca/media/img/logo.png
    :figwidth: image

Motion Média (http://motion-m.ca)
