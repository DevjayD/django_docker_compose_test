import os
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("postgres_DATABASE", 'postgres'),
        "USER": os.environ.get("postgres_USER", "postgres"),
        "PASSWORD": os.environ.get("postgres_PASSWORD", "postgres"),
        "HOST": os.environ.get("postgres_HOST", "172.18.0.2"),
        "PORT": os.environ.get("postgres_PORT", "5432"),
    }
}
