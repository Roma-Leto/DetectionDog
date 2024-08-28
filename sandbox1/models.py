# Для установки минимального значения поля Integer
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import unidecode


class OSModel(models.Model):
    """
    Таблица операционных систем
    """
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=10)  # TODO: Свой валидатор

    def __str__(self):
        return self.name


class SmartphoneModel(models.Model):
    """
    Таблица смартфонов
    """
    name = models.CharField(max_length=30, verbose_name="Название")
    price = models.FloatField()
    is_android = models.BooleanField(default=True)
    power = models.IntegerField(
        validators=[MinValueValidator(1000)],
        verbose_name='Ёмкость АКБ'
    )
    start_sale_date = models.DateField(blank=False, null=False)
    add_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    slug = models.SlugField(unique=True)
    # NOTE: Прописывается зависимость от первичной модели.
    # В виде строки потому, что первичная модель описана нижу в коде программы.
    category = models.ForeignKey(
        'CategorySmartModel',
        on_delete=models.PROTECT,  # Запись не удаляется при удалении
        # первичной модели
        related_name="categories"  # Атрибут, который позволяет указать
        # альтернативное имя для обратной связи.
        # Иначе использовалось бы category_set
    )
    shop = models.ForeignKey(
        'ShopModel',
        on_delete=models.PROTECT
    )
    # TODO: Тут добавить многие-ко-многим так как разные телефоны в
    #  разных магазинах и разные магазины с разными телефонами
    os = models.ForeignKey(OSModel, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.convert_to_slug(self.name.lower())
        super(SmartphoneModel, self).save(*args, **kwargs)

    @staticmethod
    def convert_to_slug(text):
        text = unidecode.unidecode(text)  # преобразование кириллицы в латиницу
        return slugify(text)  # формирование слага


class ShopModel(models.Model):
    """
    Таблица магазинов
    """
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name


class MakerModel(models.Model):
    """
    Таблица производителей смартфонов
    """
    name = models.CharField(max_length=50)
    country = models.ForeignKey(
        'CountryModel',
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return self.name


class CountryModel(models.Model):
    """
    Таблица стран продающих смартфон
    """
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class CategorySmartModel(models.Model):
    """
    Таблица категории смартфонов (премиум, для детей и пр.)
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.convert_to_slug(self.name.lower())
        super(CategorySmartModel, self).save(*args, **kwargs)

    @staticmethod
    def convert_to_slug(text):
        text = unidecode.unidecode(text)  # преобразование кириллицы в латиницу
        return slugify(text)  # формирование слага

    def get_absolute_url(self):
        return reverse('categories-smart', kwargs={'cat_slug': self.slug})

# NOTE: Смещение вертикальной полосы в IDE - CTRL+ALT+s -> Code Style -> Wrap
# NOTE: Нормализация — это процесс организации данных в базе данных,
#  Она включает в себя создание таблиц и установление связей между ними
#  в соответствии с правилами
# NOTE: В большинстве БД создание индексов используется для уменьшения времени
#  поиска. Если в таблице есть столбец, который часто
#  участвует в запросах `WHERE`, то создавая индекс по этому столбцу можно
#  повысить скорость выполнения этих запросов.
