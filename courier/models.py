# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.translation import gettext as _

from courier.conf import settings


class EmailTemplate(models.Model):
    """
    EmailTemplate are standard text email template
    stored in database for easier editing. Their are
    rendered as template with the sender object as context.
    """
    subject   = models.CharField(_('Subject'), max_length=250)
    slug      = models.CharField(_('Slug'), max_length=50, unique=True)
    body      = models.TextField(_('Body'), blank=True, null=True, help_text=_('Ex: Hello {{ object.firstname }} !'))
    variables = models.TextField(_('Variables'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.slug

    class Meta:
        verbose_name = _('Email template')
        verbose_name_plural = _('Email templates')


class EmailNotification(models.Model):
    """
    An EmailNotification binds a content_type, a signal and 
    a template together.
    """
    SIGNAL_CHOICES = (
        ('post_create', _('Created')), # Dummy signal
        ('post_save',   _('Modified')),
        ('post_delete', _('Deleted')),
    )
    title        = models.CharField(_('Title'), max_length=250, unique=True, help_text=_('This field is used for your reference only.'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Model'))
    signal       = models.CharField(_('Send when'), max_length=250, choices=SIGNAL_CHOICES, default="post_create")
    template     = models.ForeignKey(EmailTemplate, verbose_name=_('Template'), null=True, blank=True, on_delete=getattr(models, settings.EMAILTEMPLATE_ON_DELETE))
    recipients   = models.CharField(_('Recipients'), max_length=250, default="DEFAULT_EMAIL_TO", help_text=_('Ex: some@email.com, another@email.com, object.email, DEFAULT_EMAIL_TO'))
    from_email   = models.CharField(_('From email'), max_length=250, default=settings.DEFAULT_EMAIL_FROM)
    object_name  = models.CharField(_('Template object name'), max_length=150, default='object')
    is_active    = models.BooleanField(_('Is active'), default=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = _('Email notification')
        verbose_name_plural = _('Email notifications')


try:
    # Do not try to attach signals if the database 
    # is not yet synched
    from django.db import connection
    cursor = connection.cursor()
    if not cursor:
        raise Exception
    table_names = connection.introspection.get_table_list(cursor)
except:
    pass
else:
    from django.db.models.signals import post_save, pre_save, pre_delete
    from courier.utils import attach_signals, attach_signal, detach_signal
    from django.utils import simplejson as json

    def get_context_object_vars(model, inst):
        out = {
            'site': ['name', 'domain'],
            '%s' % inst.object_name: [],
        }
        
        fields = model._meta.get_all_field_names()
        for field in fields:
            if not field.startswith('_'):
                try:
                    out[inst.object_name].append(field)
                except AttributeError:
                    out[inst.object_name].append('%s_set.all' % field)
                except:
                    pass
        for method in dir(model.__class__):
            if method not in fields and \
                    not method.startswith('_') and \
                    method not in settings.IGNORED_CONTEXT_METHODS:
                out[inst.object_name].append(method)
        return json.dumps(out)

    @receiver(pre_save, sender=EmailNotification, dispatch_uid="courier.email_notification_pre_save")
    def email_notification_pre_save(sender, **kwargs):
        instance = kwargs['instance']
        detach_signal(instance.signal, instance.content_type.pk)

    @receiver(pre_delete, sender=EmailNotification, dispatch_uid="courier.email_notification_post_delete")
    def email_notification_post_delete(sender, **kwargs):
        instance = kwargs['instance']
        detach_signal(instance.signal, instance.content_type.pk)


    @receiver(post_save, sender=EmailNotification, dispatch_uid="courier.email_notification_post_save")
    def email_notification_post_save(sender, **kwargs):
        instance = kwargs['instance']
        if instance.template:
            model = instance.content_type.model_class()
            if model:
                attach_signal(instance.signal, instance.content_type.pk)
               #instance.template.variables = u'site_name, site_domain, %s (%s)' % (instance.object_name, get_context_object_vars(model))
                instance.template.variables = get_context_object_vars(model, instance)
                instance.template.save()

    # Attach all signals on startup
    if 'courier_emailnotification' in table_names:
        attach_signals(EmailNotification.objects.values('signal', 'content_type').distinct())
