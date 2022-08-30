from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    '''Покемон'''
    title = models.CharField('Покемон', max_length=200)

    def __str__(self):
        return f'{self.title}'
