4\.B ZŠ Žerotínova z Valašského Meziříčí opět v akci.

Instalace
=========

Derby jsou [Django][https://www.djangoproject.com/] aplikace (takže musíš mít aspoň
Python 2.7 a nainstalované balíčky z adresáře `requirements`).

Do adresáře `derby` ulož soubor `settings.py`, a doplň patřičné údaje:

    from .common_settings import *

    SECRET_KEY = 'ZMETZNAKU' # viz https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-SECRET_KEY

    # pripojeni k databazi   # viz https://docs.djangoproject.com/en/1.7/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # vypnuti debug rezimu
    DEBUG = False
    TEMPLATE_DEBUG = False

    # kdo se muze divat na web? vsichni!
    ALLOWED_HOSTS = ['*']   # viz https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-ALLOWED_HOSTS
