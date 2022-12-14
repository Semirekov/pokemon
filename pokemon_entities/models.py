from django.db import models  # noqa F401


class Pokemon(models.Model):
    '''Покемон'''
    
    title = models.CharField('Покемон', max_length=200)
    photo = models.ImageField(
        verbose_name='Картинка', 
        upload_to='pokemons',         
        blank=True,
    )
    description = models.TextField('Описание', blank=True,)
    title_en = models.CharField(
        'Покемон (англ.)', 
        max_length=64,         
        blank=True
    )
    title_jp = models.CharField(
        'Покемон (яп.)', 
        max_length=64,         
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
        related_name='entities',
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

    def get_photo_absolute_uri(self, request):
        if self.pokemon and self.pokemon.photo:
            return request.build_absolute_uri(self.pokemon.photo.url)
    
        return ''