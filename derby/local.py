SECRET_KEY = 'gdav1@2b!8veka=)xc8)tqjwj1s11&_3&*a5wde_rua_72_zww'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'cs-CZ'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "uploads"),
)
#MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/uploads/'


LOGIN_URL = '/prihlaseni/'


import redis
REDIS = redis.Redis()
