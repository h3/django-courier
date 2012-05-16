import logging, datetime

from django.db.models import signals
from django.db.models import get_model 
from django.core.mail import send_mail
from django.template import Context, Template
from courier.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

#from contrib.core.debug import brake

log = logging.getLogger('courier')

def parse_recipients(r, inst):
    out = []
    emails = map(lambda x: x.strip(), r.split(','))
    
    def get_email(e, inst):
        if e.startswith('object.'):
            try:
                return inst.__getattribute__(e[7:])
            except:
                return False
        elif e == 'DEFAULT_EMAIL_TO':
            if hasattr(settings, 'DEFAULT_EMAIL_TO'):
                return settings.DEFAULT_EMAIL_TO
            else:
                return False
        else:
            return e

    for email in emails:
        e = get_email(email, inst)
        if e:
            if isinstance(e, list) :
                out.extend(e)
            else:
                out.append(e)
    return out


def attach_signal(signal_name, content_type_pk):
    """
    Attach a given signal to a content type
    """
    ct    = ContentType.objects.get(pk=content_type_pk)
    model = ct.model_class()
    if model:
        app = ct.app_label
        uid = '%s.%s.%s' % (app, signal_name, content_type_pk)

        if signal_name == 'post_create':
            dispatcher = created_dispatcher
            signal = getattr(signals, 'post_save')
        else:
            signal = getattr(signals, signal_name)
            if signal_name == 'post_delete':
                dispatcher = deleted_dispatcher
            else:
                dispatcher = modified_dispatcher

        signal.connect(dispatcher, sender=model, dispatch_uid=uid)
        log.debug("Courier: Attached %s on %s.%s (uid %s)" % (signal_name, app, model.__name__, uid) )


def attach_signals(signal_list):
    """
    Attach a list of signals to content types
    """
    for s in signal_list:
        attach_signal(s['signal'], s['content_type'])


def detach_signal(signal_name, content_type_pk):
    """
    Attach a given signal to a content type
    """
    ct    = ContentType.objects.get(pk=content_type_pk)
    model = ct.model_class()
    if model:
        app = ct.app_label
        uid = '%s.%s.%s' % (app, signal_name, content_type_pk)

        if signal_name == 'post_create':
            dispatcher = created_dispatcher
            signal = getattr(signals, 'post_save')
        else:
            signal = getattr(signals, signal_name)
            if signal_name == 'post_delete':
                dispatcher = deleted_dispatcher
            else:
                dispatcher = modified_dispatcher

        signal.disconnect(dispatcher, sender=model, dispatch_uid=uid)
        log.debug("Courier: Detached %s.%s on %s (uid %s)" % (signal_name, app, model.__name__, uid) )


# Signal dispatchers

def get_dispatcher_context(kwargs, signal):
    ct = ContentType.objects.get_for_model(kwargs['instance'])
    return (kwargs['instance'], ct,
            # avoid circular reference
            get_model('courier', 'EmailNotification').objects.\
                    filter(content_type__pk=ct.pk, signal=signal, is_active=True))


def created_dispatcher(sender, **kwargs):
    if kwargs['created'] == True:
        instance, ct, notifications = get_dispatcher_context(kwargs, 'post_create')
        for notification in notifications:
            send_notification(notification, instance, 'created')


def modified_dispatcher(sender, **kwargs):
    instance, ct, notifications = get_dispatcher_context(kwargs, 'post_save')
    if kwargs['created'] == False:
        for notification in notifications:
            send_notification(notification, instance, 'modified')


def deleted_dispatcher(sender, **kwargs):
    instance, ct, notifications = get_dispatcher_context(kwargs, 'post_delete')
    for notification in notifications:
        send_notification(notification, instance, 'deleted')


def send_notification(notification, instance, created=False):
    """
    This is the actual method that sends the notifications
    """

    site       = Site.objects.get(id=settings.SITE_ID)
    template   = notification.template
    recipients = parse_recipients(notification.recipients, instance)
    subject    = Template(template.subject).render(Context({
        '%s' % notification.object_name: instance,
        'site_name': site.name,
        'site_domain': site.domain,
    }))
    body       = Template(template.body).render(Context({
        '%s' % notification.object_name: instance,
        'site_name': site.name,
        'site_domain': site.domain,
    }))

    start_time = datetime.datetime.today()
    log.debug(u"Courier: trying to send \"%s\" notification to %s from %s" % (subject, ", ".join(recipients), notification.from_email))

    send_mail(subject, body, notification.from_email, recipients, fail_silently=settings.FAIL_SILENTLY)

    end_time = datetime.datetime.today()
    log.debug(u"Courier: \"%s\" notification sent to %s from %s (%ss)" % (subject, ", ".join(recipients), notification.from_email, end_time - start_time))
