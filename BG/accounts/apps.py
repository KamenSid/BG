from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BG.accounts'

    def ready(self):
        import BG.accounts.signals
