from django.db import models

# Create your models here.


class Lesson(models.Model):

    note_id = models.SmallIntegerField(default=1,
                                       verbose_name='Порядковый номер')
    title = models.CharField(max_length=150,
                             verbose_name='Образовательный модуль')
    description = models.TextField(verbose_name='Описание модуля')

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        verbose_name = 'образовательный модуль'
        verbose_name_plural = 'образовательные модули'
