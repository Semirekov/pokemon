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
    pokemon = models.ForeignKey(
        Pokemon,
        null=False,
        verbose_name='Покемон',
        on_delete=models.CASCADE)
    lat = models.FloatField('Широта', null=True)
    lon = models.FloatField('Долгота', null=True)
    level = models.IntegerField('Уровень', null=True)
    health = models.IntegerField('Здоровье', null=True)
    strenght = models.IntegerField('Атака', null=True)
    defence = models.IntegerField('Защита', null=True)
    stamina = models.IntegerField('Выносливость', null=True)
    appeared_at = models.DateTimeField(null=False)
    disappeared_at = models.DateTimeField(null=True)