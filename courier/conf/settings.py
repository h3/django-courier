from django.conf import settings

SITE_ID = getattr(settings, 'SITE_ID', 1) # Just needs to pass it around
FAIL_SILENTLY = getattr(settings, 'COURIER_FAIL_SILENTLY', True)
IGNORED_CONTEXT_METHODS = getattr(settings, 'COURIER_IGNORED_CONTEXT_METHODS', ['add_to_class', 'copy_managers', 'mro'])
EMAILTEMPLATE_ON_DELETE = getattr(settings, 'COURIER_EMAILTEMPLATE_ON_DELETE', 'SET_NULL')

if hasattr(settings, 'COURIER_DEFAULT_EMAIL_FROM'):
    DEFAULT_EMAIL_FROM = settings.COURIER_DEFAULT_EMAIL_FROM
else:
    try:
        from django.contrib.sites.models import Site
        site = Site.objects.get(id=settings.SITE_ID)
        DEFAULT_EMAIL_FROM = 'no-reply@%s' % site.domain
    except:
        # In theory, this should never happen unless the
        # Django site framework isn't installed
        DEFAULT_EMAIL_FROM = 'no-reply@courier.com'


if hasattr(settings, 'COURIER_DEFAULT_EMAIL_TO'):
    DEFAULT_EMAIL_TO = settings.COURIER_DEFAULT_EMAIL_TO
elif hasattr(settings, 'ADMINS'):
    DEFAULT_EMAIL_TO = []
    for admin in settings.ADMINS:
        DEFAULT_EMAIL_TO.append(admin[1])
