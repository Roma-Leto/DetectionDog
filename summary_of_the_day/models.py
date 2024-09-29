from django.db import models


class Cigarettes(models.Model):
    data = models.DateField(verbose_name="Дата", unique=True)
    count = models.IntegerField(
        verbose_name="Количество",
        blank=False,
        null=False,
    )


class PullUpsModel(models.Model):
    data = models.DateField(verbose_name="Дата")
    count = models.IntegerField(
        verbose_name="Количество подтягиваний",
        blank=False,
        null=False,
    )
    number_of_approaches = models.IntegerField(
        default=0,
        verbose_name="Подход"
    )

    # def save(self, *args, **kwargs):
    #     self.number_of_approaches += 1
    #     super().save(*args, **kwargs)

