from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    '''Покемон'''
    title = models.CharField('Покемон', max_length=200)
    photo = models.ImageField(upload_to='pokemons', null=True)

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    '''Положение на карте'''
    lat = models.FloatField('Широта', null=True)
    lon = models.FloatField('Долгота', null=True)
    pokemon = models.ForeignKey(
        Pokemon,
        null=False,
        verbose_name='Покемон',
        on_delete=models.CASCADE)