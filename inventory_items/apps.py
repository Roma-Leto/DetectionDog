from django.apps import AppConfig


class InventoryItemsConfig(AppConfig):
    """
    Конфигурация приложения Inventory Items.

    Этот класс управляет настройками приложения inventory_items,
    включая автоматическое поле по умолчанию для моделей.

    Атрибуты:
        default_auto_field (str): Поле, используемое по умолчанию для
                                автоинкрементных идентификаторов.
        name (str): Полное имя приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_items'
