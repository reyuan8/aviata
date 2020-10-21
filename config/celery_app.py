import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.apps import AppConfig, apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("aviata")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


class CeleryAppConfig(AppConfig):
    name = "aviata.config"
    verbose_name = "Celery Config"

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
