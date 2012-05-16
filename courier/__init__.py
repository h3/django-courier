from django.conf import settings

if 'modeltranslation' in settings.INSTALLED_APPS:
    try:
        from modeltranslation.translator import translator, TranslationOptions
        from courier.models import EmailTemplate

        class EmailTemplateTranslationOptions(TranslationOptions):
            fields = ('subject', 'body',)
        translator.register(EmailTemplate, EmailTemplateTranslationOptions)
    except:
        pass
