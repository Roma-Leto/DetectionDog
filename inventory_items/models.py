__all__ = [
    'ItemModel',
    'CategoryModel',
    'MaterialBoxModel',
    'BoxModel',
    'LocationModel'
]

from django.db import models
from django.urls import reverse

# region Модель локации
class LocationModel(models.Model):
    """
    Модель, представляющая локацию для хранения предметов.

    Атрибуты:
        name (str): Название места, уникальное значение.
    """

    name = models.CharField(max_length=30,
                            verbose_name="Название места",
                            blank=False,
                            null=False,
                            unique=True)

    def get_absolute_url(self):
        """Возвращает URL для детальной информации о локации."""
        return reverse('inventory:location-details', kwargs={'pk': self.id})

    @classmethod
    def get_default_location(cls):
        """Возвращает первую (по умолчанию) локацию из базы данных."""
        return cls.objects.first()

    @classmethod
    def get_last_location_item(cls):
        """Возвращает последнюю локацию, связанную с предметом."""
        return ItemModel.objects.first().location

    def __str__(self):
        """Возвращает строковое представление локации."""
        return self.name

    class Meta:
        ordering = ["-id"]


# endregion

# region Модель бокса
class BoxModel(models.Model):
    """
    Модель, представляющая коробку или упаковку для предметов.

    Атрибуты:
        number (str): Номер коробки, уникальное значение.
        width (int): Ширина бокса.
        height (int): Высота бокса.
        depth (int): Глубина бокса (по умолчанию 0).
        details (str): Описание бокса.
        photo (ImageField): Фото бокса.
        material (ForeignKey): Связь с моделью материала упаковки.
        location (ForeignKey): Связь с моделью локации.
    """

    number = models.CharField(max_length=30,
                              verbose_name="Номер коробки/пакета",
                              blank=False,
                              null=False,
                              unique=True)
    width = models.IntegerField(verbose_name='Ширина бокса/пакета',
                                blank=False,
                                null=False)
    height = models.IntegerField(verbose_name='Высота бокса/пакета',
                                 blank=False,
                                 null=False)
    depth = models.IntegerField(verbose_name='Глубина бокса',
                                blank=False,
                                default=0)
    details = models.TextField(verbose_name="Описание",
                               blank=True)
    photo = models.ImageField(upload_to="uploads/box/%Y/%m/%d",
                              verbose_name='Фото',
                              blank=True,
                              null=True,
                              default=None)

    material = models.ForeignKey("MaterialBoxModel",
                                 verbose_name="Материал",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    location = models.ForeignKey(LocationModel,
                                 verbose_name="Место/локация",
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True)

    def get_absolute_url(self):
        """Возвращает URL для детальной информации о боксе."""
        return reverse('inventory:box-details', kwargs={'pk': self.id})

    def __str__(self):
        """Возвращает строковое представление бокса."""
        return self.number

    class Meta:
        ordering = ["-id"]

    @classmethod
    def get_default_box(cls):
        """Возвращает первый (по умолчанию) бокс из базы данных."""
        return cls.objects.first()

    @classmethod
    def get_last_box_item(cls):
        """Возвращает последний бокс, связанный с предметом."""
        return ItemModel.objects.first().box


# endregion

# region Модель материалов упаковки
class MaterialBoxModel(models.Model):
    """
    Модель, представляющая материал упаковки.

    Атрибуты:
        name (str): Название материала, уникальное значение.
        moisture_protection (bool): Флаг, указывающий на влагозащиту.
    """

    name = models.CharField(max_length=30,
                            verbose_name="Название материала упаковки",
                            blank=False,
                            null=False,
                            unique=True)
    moisture_protection = models.BooleanField(verbose_name="Влагозащита")

    def get_absolute_url(self):
        """Возвращает URL для детальной информации о материале упаковки."""
        return reverse('inventory:material-details', kwargs={'pk': self.pk})

    def __str__(self):
        """Возвращает строковое представление материала упаковки."""
        return self.name


# endregion

# region Модель категорий
class CategoryModel(models.Model):
    """
    Модель, представляющая категорию предметов.

    Атрибуты:
        name (str): Название категории, уникальное значение.
    """

    name = models.CharField(max_length=30,
                            verbose_name="Название категории",
                            blank=False,
                            null=False,
                            unique=True)

    def get_absolute_url(self):
        """Возвращает URL для детальной информации о категории."""
        return reverse("inventory:category-details", kwargs={"pk": self.pk})

    @classmethod
    def get_last_cat_item(cls):
        """Возвращает последнюю категорию, связанную с предметом."""
        return ItemModel.objects.first().categories

    def __str__(self):
        """Возвращает строковое представление категории."""
        return self.name


# endregion

# region Модель предмета
class ItemModel(models.Model):
    """
    Модель, представляющая предмет.

    Атрибуты:
        name (str): Название предмета.
        photo (ImageField): Фото предмета.
        details (str): Описание предмета.
        date_create (DateTimeField): Время добавления предмета.
        count (int): Количество или объем предмета.
        status (str): Статус предмета (например, "В наличии").
        categories (ForeignKey): Связь с моделью категории.
        box (ForeignKey): Связь с моделью бокса.
        location (ForeignKey): Связь с моделью локации.
    """

    name = models.CharField(max_length=30,
                            verbose_name="Название предмета",
                            blank=False)
    photo = models.ImageField(verbose_name="Фотография",
                              blank=True,
                              upload_to='uploads/%Y/%m/%d',
                              null=True,
                              default='uploads/default_item_image.png')
    details = models.TextField(verbose_name="Описание предмета")
    date_create = models.DateTimeField(verbose_name="Время добавления",
                                       auto_now_add=True)
    count = models.IntegerField(verbose_name="Количество/Объём",
                                blank=True,
                                default=1)

    STATUS_OF_ITEM = {
        "exist": "В наличии",
        "recycled": "Переработано",
        "thrown": "Выброшено"
    }

    status = models.CharField(max_length=15,
                              verbose_name="Статус",
                              blank=True,
                              null=False,
                              choices=STATUS_OF_ITEM,
                              default="exist")
    categories = models.ForeignKey(CategoryModel,
                                   verbose_name="Категория предмета",
                                   on_delete=models.PROTECT,
                                   blank=True,
                                   null=True,
                                   default=CategoryModel.get_last_cat_item)

    box = models.ForeignKey(BoxModel,
                            on_delete=models.PROTECT,
                            verbose_name="Упаковка",
                            blank=True,
                            null=True,
                            default=BoxModel.get_last_box_item)

    location = models.ForeignKey(LocationModel,
                                 verbose_name="Место/локация",
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 default=LocationModel.get_last_location_item)

    def get_absolute_url(self):
        """Возвращает URL для детальной информации о предмете."""
        return reverse('inventory:item-details', kwargs={"pk": self.pk})

    @classmethod
    def get_last_item(cls):
        """Возвращает последний добавленный предмет."""
        last_item = cls.objects.last()
        return last_item

    def __str__(self):
        """Возвращает строковое представление предмета."""
        return self.name

    class Meta:
        ordering = ['-id']

# endregion
