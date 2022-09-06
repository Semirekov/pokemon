from django.db import models  # noqa F401


class Pokemon(models.Model):
    '''Покемон'''
    
    title = models.CharField('Покемон', max_length=200)
    photo = models.ImageField(
        verbose_name='Картинка', 
        upload_to='pokemons', 
        null=True, 
        blank=True,
    )
    description = models.TextField('Описание', null=True, blank=True,)
    title_en = models.CharField(
        'Покемон (англ.)', 
        max_length=64, 
        null=True, 
        blank=True
    )
    title_jp = models.CharField(
        'Покемон (яп.)', 
        max_length=64, 
        null=True, 
        blank=True
    )
    next_evolution = models.ForeignKey(
        'self', 
        verbose_name='Эволюционирует в',
        related_name='nextstage',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    '''Положение на карте'''    
    pokemon = models.ForeignKey(
        Pokemon,
        related_name='pokemons',
        verbose_name='Покемон',
        on_delete=models.CASCADE)

    lat = models.FloatField('Широта',)
    lon = models.FloatField('Долгота',)
    level = models.IntegerField('Уровень', null=True, blank=True,)
    health = models.IntegerField('Здоровье', null=True, blank=True,)
    strenght = models.IntegerField('Атака', null=True, blank=True,)
    defence = models.IntegerField('Защита', null=True, blank=True,)
    stamina = models.IntegerField('Выносливость', null=True, blank=True,)
    appeared_at = models.DateTimeField('Появится',)
    disappeared_at = models.DateTimeField('Исчезнет',)    