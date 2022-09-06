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


def get_info_evolution(request, pokemon):
    return {
        'title_ru': pokemon.title,
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url if pokemon.photo else '',  
    }


def get_next_evolution(request, pokemon):    
    if not pokemon.next_evolution:
        return   
        
    return get_info_evolution(
        request, 
        Pokemon.objects.get(id=pokemon.next_evolution.id)
    )


def get_previous_evolution(request, pokemon):    
    parent = Pokemon.objects.filter(next_evolution=pokemon.id)
    if parent.count() != 1:
        return

    return get_info_evolution(
        request, 
        parent.first()
    ) 


def show_pokemon(request, pokemon_id):
    timenow = localtime()      
    pokemon_entity = PokemonEntity.objects.filter(
        pokemon_id=pokemon_id,
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

    pokemon = Pokemon.objects.get(id=pokemon_id)
    
    pokemon = {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else '',
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'next_evolution': get_next_evolution(request, pokemon),
            'previous_evolution': get_previous_evolution(request, pokemon),
    }
    

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
