:tocdepth: 2

.. _debugging:

Debugging
=========

To see debug output in your console when using the development server, just add a logger named `courier` in your `settings.py`.

Example::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'courier': {
                'handlers': ['mail_admins', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }
