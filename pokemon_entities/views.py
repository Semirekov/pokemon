import folium


from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    timenow = localtime()    
    pokemon_entity = PokemonEntity.objects.filter(
        appeared_at__lt=timenow, 
        disappeared_at__gt=timenow        
    )
    
    for entity in pokemon_entity:
        
        add_pokemon(
            folium_map, 
            entity.lat,
            entity.lon,      
            entity.get_photo_absolute_uri(request)            
        )
        
    pokemons_on_page = []
    for pokemon in pokemons:             
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else '',
            'title_ru': pokemon.title
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def get_info_evolution(pokemon):
    return {
        'title_ru': pokemon.title,
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url if pokemon.photo else '',  
    }


def show_pokemon(request, pokemon_id):
    timenow = localtime()   
    pokemon = Pokemon.objects.get(id=pokemon_id)

    pokemon_entity =  pokemon.entities.filter(        
        appeared_at__lt=timenow, 
        disappeared_at__gt=timenow        
    )
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entity:        
        add_pokemon(
            folium_map, 
            entity.lat,
            entity.lon,
            entity.get_photo_absolute_uri(request)
        )
    
    next_evolution = {}
    if pokemon.next_evolution:
        next_stage = Pokemon.objects.get(id=pokemon.next_evolution.id)
        next_evolution = {
            'title_ru': next_stage.title,
            'pokemon_id': next_stage.id,
            'img_url': next_stage.photo.url if next_stage.photo else '',  
        }

    prev_evolution = {}    
    prevstages = Pokemon.objects.filter(next_evolution=pokemon.id)    
    if prevstages.count() == 1:            
        prevstage = prevstages.first()
        prev_evolution = {
            'title_ru': prevstage.title,
            'pokemon_id': prevstage.id,
            'img_url': prevstage.photo.url if prevstage.photo else '',  
        }

    pokemon_info = {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else '',
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'next_evolution': next_evolution, 
            'previous_evolution': prev_evolution 
    }
    

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
