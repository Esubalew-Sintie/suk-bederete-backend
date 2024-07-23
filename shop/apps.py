from django.apps import AppConfig

class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        import shop.signals  # Ensure that signals are imported
