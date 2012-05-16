:tocdepth: 2

.. _installation:

Introduction
============

For easier management of development and production environments I suggest to 
use a variable named `DEV` in your `settings.py`. This is technique optional, 
but the following examples will use it. Obviously, if `DEV` is True it means 
we are running it a development environment.

The key difference between `DEV` and `DEBUG` is that sometimes you need to set
`DEBUG` to True in the production environment to troubleshoot a problem while 
`DEV` should _never_ be True when in production.

The `settings.py` should contain something like this::

    DEV = True
    DEBUG = DEV
    TEMPLATE_DEBUG = DEBUG


Installation
============

Just add `'courier'` in your `settings.INSTALLED_APPS` and sync your database.

Django email settings example
-----------------------------

Courier will use standard Django configurations::

    if DEV:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        COURIER_FAIL_SILENTLY = False
    else:
        EMAIL_HOST = 'smtp.example.com'
        EMAIL_PORT = 45
        EMAIL_HOST_USER = 'no-reply@example.com'
        EMAIL_HOST_PASSWORD = 'mypassword'
        EMAIL_USE_TLS = False


Courier settings
----------------

These settings are all optional.

+-----------------------------------+----------------------------+----------------------------------------------------------------------------+
| Setting                           | Default                    | Description                                                                |
+===================================+============================+============================================================================+
| `COURIER_FAIL_SILENTLY`           | True                       | Weather or not to fail silently when sending emails                        |
+-----------------------------------+----------------------------+----------------------------------------------------------------------------+
| `COURIER_DEFAULT_EMAIL_FROM`      | `'no-reply@example.com'`   | Default "email from" to use (can be overridden for each EmailNotification) |
+-----------------------------------+----------------------------+----------------------------------------------------------------------------+
| `COURIER_DEFAULT_EMAIL_TO`        | settings.ADMINS emails     | Default "email to" to use (can be overridden for each EmailNotification)   |
+-----------------------------------+----------------------------+----------------------------------------------------------------------------+
| `COURIER_IGNORED_CONTEXT_METHODS` | ['add_to_class',           | Methods that should not show up in template variables helper (Warning:     |
|                                   |   'copy_managers', 'mro']  | they are still available from the context)                                 |
+-----------------------------------+----------------------------+----------------------------------------------------------------------------+
| `COURIER_EMAILTEMPLATE_ON_DELETE` | `'SET_NULL'`               | Defines what happens when an email template linked to an email             |
|                                   |                            | notification is deleted (can be `SET_DEFAULT`, `CASCADE`, `PROTECT`,       |
|                                   |                            | `SET_NULL` or `DO_NOTHING`\*)                                              |
+-----------------------------------+----------------------------+----------------------------------------------------------------------------+

 \* https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete
