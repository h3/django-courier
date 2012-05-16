# -*- coding: utf-8 -*-

"""
Courrier pre-packaged grappelli dashboard modules
"""

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules

courier_module_children = []

courier_email_confs = modules.ModelList(
    _('Courier configurations'),
    column=1,
    collapsible=True,
#   css_classes=('collapse closed',),
    models=(
        'courier.models.EmailTemplate',
        'courier.models.EmailNotification',
    ),
)

courier_module_children.append(courier_email_confs)

courier_module = modules.Group(_('Courier'),
    column = 1,
    collapsible = True,
    children = courier_module_children
)

