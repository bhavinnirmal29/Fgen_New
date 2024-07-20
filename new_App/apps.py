from django.apps import AppConfig


class NewAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "new_App"
    def ready(self):
        import new_App.signals