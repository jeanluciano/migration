
from operator import imod
from prefect import flow,task
from prefect.task_runners import SequentialTaskRunner
from prefect.tasks import task_input_hash

import requests


@task(cache_key_fn=task_input_hash)
def find_species(name):
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/').json()
    return r['species']['name']

@task(cache_key_fn=task_input_hash)
def find_egg_groups(species_name:str):
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{species_name}/').json()
    return [group['name'] for group in r['egg_groups']]

@task()
def get_compatible_species(egg):
    r = requests.get(f'https://pokeapi.co/api/v2/egg-group/{egg}').json()
    return r

@task()
def save_to_file(species):
    with open('pokemon.txt','w+') as file:
        file.write(species)
    return


@flow(name="Pokebreeder", task_runner=SequentialTaskRunner())
def find_breed_compatible_pokemon(pokemon):
    poke_species = find_species(pokemon)
    egg_groups = find_egg_groups(poke_species)
    compatible_species = [get_compatible_species(x).result()['pokemon_species'] for x in egg_groups.result()]
    
    



