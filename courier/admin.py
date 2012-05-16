from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from courier.models import EmailTemplate, EmailNotification

try:
    # A special fork of modeltranslation I use ..
    from contrib.core.admin import TranslationAdmin
    BaseClass = TranslationAdmin
except:
    try:
        from modeltranslation.admin import TranslationAdmin
        BaseClass = TranslationAdmin
    except:
        BaseClass = admin.ModelAdmin

class EmailNotificationInline(admin.StackedInline):
    model = EmailNotification
    extra = 1

class EmailTemplateAdmin(BaseClass):
    list_display = ('slug', 'subject', 'variables')
    search_fields = ('subject', 'slug', 'body')
    prepopulated_fields = {'slug': ('subject',)}
    inlines = [EmailNotificationInline]
    class Media:
        js = (
           #'%scourier/js/force_jquery.js' % settings.STATIC_URL,
            '%scourier/js/jquery.courier.js' % settings.STATIC_URL,
        )
        css = {
            'screen': ('%scourier/css/django.courier.css' % settings.STATIC_URL,),
        }
admin.site.register(EmailTemplate, EmailTemplateAdmin)


def desactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)
desactivate.short_description = _("Desactivate selected email notifications")

def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate.short_description = _("Activate selected email notifications")

class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'signal', 'from_email', 'recipients', 'template', 'is_active')
    search_fields = ('title', )
    list_filter = ('is_active', 'signal')
    actions = [activate, desactivate]
admin.site.register(EmailNotification, EmailNotificationAdmin)


