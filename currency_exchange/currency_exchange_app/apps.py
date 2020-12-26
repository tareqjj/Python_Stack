from django.apps import AppConfig


class CurrencyExchangeAppConfig(AppConfig):
    name = 'currency_exchange_app'

    def ready(self):
        from rateUpdater import updater
        updater.start()
