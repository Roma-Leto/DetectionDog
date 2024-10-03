from django.db import models

from django.urls import reverse


# region Модель локации
class LocationModel(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name="Название места",
                            blank=False,
                            null=False,
                            unique=True)

    def get_absolute_url(self):
        return reverse('inventory:location-details', kwargs={'pk': self.id})

    @classmethod
    def get_default_location(cls):
        return LocationModel.objects.first()

    @classmethod
    def get_last_location_item(cls):
        return ItemModel.objects.first().location

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


# endregion

# region Модель бокса
class BoxModel(models.Model):
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
    photo = models.ImageField(upload_to="uploads/box/%Y/%m/%d'",
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
        return reverse('inventory:box-details', kwargs={'pk': self.id})

    def __str__(self):
        return self.number

    class Meta:
        ordering = ["-id"]

    @classmethod
    def get_default_box(cls):
        return BoxModel.objects.first()

    @classmethod
    def get_last_box_item(cls):
        return ItemModel.objects.first().box


# endregion

# region Модель материалов упаковки
class MaterialBoxModel(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name="Название материала упаковки",
                            blank=False,
                            null=False,
                            unique=True)
    moisture_protection = models.BooleanField(verbose_name="Влагозащита")

    def get_absolute_url(self):
        return reverse('inventory:material-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


# endregion Модель категории

# region Модель категорий
class CategoryModel(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name="Название категории",
                            blank=False,
                            null=False,
                            unique=True)

    def get_absolute_url(self):
        return reverse("inventory:category-details", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


# endregion

# region Модель предмета
class ItemModel(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name="Название предмета",
                            blank=False, )
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
                                   null=True)

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
        return reverse('inventory:item-details', kwargs={"pk": self.pk})

    @classmethod
    def get_last_item(cls):
        last_item = ItemModel.objects.last()
        print(last_item)
        return last_item

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

# endregion

# NOTE: ctnl +/- | ctrl shift +/-
