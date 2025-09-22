"""
Django settings for core project.
"""

from pathlib import Path
import os
import dj_database_url  # ← 追加

# ====== Paths ======
BASE_DIR = Path(__file__).resolve().parent.parent

# ====== Security / Debug ======
# ローカルでは True、本番では環境変数 DEBUG=False をセット
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# 本番では必ず環境変数 SECRET_KEY を設定してください
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    # 既存の開発用キー（そのまま残しておきます）
    "django-insecure-e7$-x$=))0+5^h#p+ifc7kc5a++r%y#j#1qh-p2w&49$kw9@au",
)

# Render 等にデプロイする際は、サービスのドメインをカンマ区切りで渡してください
# 例: ALLOWED_HOSTS="127.0.0.1,localhost,your-service.onrender.com"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ====== Installed apps ======
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 追加
    "rest_framework",
    "django_filters",
    "roads",

    # 本番向け追加
    "corsheaders",  # ← 追加
]

# ====== Middleware ======
# 注意：順序が重要
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← 追加：SecurityMiddleware の直後
    'corsheaders.middleware.CorsMiddleware',        # ← 追加：CommonMiddleware より前
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ====== Templates ======
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],   # アプリ内 templates/ を自動探索（APP_DIRS=True）
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ====== Database ======
# デフォルトは SQLite（ローカル開発）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : BASE_DIR / 'db.sqlite3',
    }
}
# 本番（PostgreSQL など）に切り替え：環境変数 DATABASE_URL があれば上書き
# 例: postgres://USER:PASSWORD@HOST:PORT/DBNAME
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,                  # 接続再利用
        ssl_require=not DEBUG,             # 本番でSSL
    )

# ====== Password validation ======
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====== I18N / TZ ======
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'           # 必要なら 'Asia/Tokyo' に変更OK
USE_I18N = True
USE_TZ = True

# ====== Static files (WhiteNoise) ======
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ====== CORS ======
# 後で独自フロントを別ドメインに置く場合に備えて許可
# 公開後は必要なドメインのみに絞る（例：CORS_ALLOWED_ORIGINS = ["https://your-frontend.com"])
CORS_ALLOW_ALL_ORIGINS = True

# ====== CSRF (本番のドメインを登録) ======
# 例: CSRF_TRUSTED_ORIGINS="https://your-service.onrender.com"
CSRF_TRUSTED_ORIGINS = (
    os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if os.getenv("CSRF_TRUSTED_ORIGINS")
    else []
)

# ====== Default primary key ======
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'