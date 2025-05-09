import os
from pathlib import Path

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات الأمان
SECRET_KEY = 'django-insecure-very-secret-key'  # استبدله بمفتاح حقيقي في الإنتاج
DEBUG = True
ALLOWED_HOSTS = ['*']

 
# التطبيقات المثبتة
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'django_extensions',

    # Project apps
    'requests.apps.RequestsConfig',  # تطبيق الطلبات
    'website', # تطبيق الموقع الرسمي
    'admin_panel', # تطبيق لوحة الادارة
    'accounts.apps.AccountsConfig', # تطبيق الحسابات
    'client_panel', # تطبيق العملاء
    'contracts.apps.ContractsConfig', # تطبيق العقود
    'reports.apps.ReportsConfig', # تطبيق التقارير
]

# إعدادات الوسيط (Middleware)
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',  # أضف هذا في الأعلى
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# إعدادات الروابط
ROOT_URLCONF = 'advard.urls'

# إعداد القوالب (Templates)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ربط القوالب داخل مجلد templates في backend
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                 'accounts.context_processors.user_avatar',
            ],
        },
    },
]



# إعداد قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),  # تحويل المسار إلى string لتجنب الخطأ

    }
}

# إعدادات ملفات الاستاتيك
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),           # للبيئة المحلية
    os.path.join(BASE_DIR, "backend", "static") # للإنتاج

]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ جديد


LOGOUT_REDIRECT_URL = '/'


# إعدادات WSGI
WSGI_APPLICATION = 'advard.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#  اعدادات اللغة

USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
]

LANGUAGE_CODE = 'ar'

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # أو المسار المناسب حسب مشروعك
]


#  خاص  بربط الايميل الرسمي للشركة

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.sa'  # أو smtp.zoho.sa لو كان حسابك سعودي
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'admin@advardsystem.com'
EMAIL_HOST_PASSWORD = 'Kch9vQJMJdD7'
DEFAULT_FROM_EMAIL = 'Advard System <admin@advardsystem.com>'



#  خاص بتطبيق الحاسابات

AUTH_USER_MODEL = 'accounts.CustomUser'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


