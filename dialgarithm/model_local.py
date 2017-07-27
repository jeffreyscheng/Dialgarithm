from .dex import *
import math


class Model:
    # this has been running: 12.0038711684 27.0861221799 0.146702094589 0.0454514591832
    # constants
    time_per_battle = 20 / 1000  # from EC2 instance and personal laptop
    evolution_time = 5 * 60

    # ids
    date = None
    link = None
    path = None
    gen = None
    format = None

    # user inputs
    core = []

    # meta
    dex = None
    moveset_dict = None
    moveset_list = None
    usage_dict = None
    counters_dict = None
    mutation_dict = {}
    move_cache = None
    switch_cache = None
    damage_cache = {}
    elo_dict = None

    # hyperparameters
    starting_mutation_rate = 0.1
    mutation_delta = 0
    population_size = 10
    num_generations = 1
    matches = 5

    mutation_prob = starting_mutation_rate

    # outputs
    metagame = None
    recommendations = None

    @staticmethod
    def set_path():
        Model.path = "./" + Model.date + Model.link

    @staticmethod
    def set_link(link):
        Model.link = link
        name = link.split('.')[0]
        sections = name.split('-')
        gen_format = sections[0]
        head = gen_format[0:3]
        if head == 'gen':
            index = int(gen_format[3])
            if index == 3:
                Model.gen = 'rs'
            elif index == 4:
                Model.gen = 'dp'
            elif index == 5:
                Model.gen = 'bw'
            elif index == 6:
                Model.gen = 'xy'
            elif index == 7:
                Model.gen = 'sm'
            else:
                print('invalid gen!')
            Model.format = Format(gen_format[4:])
        else:
            Model.gen = 'xy'
            Model.format = Format(gen_format)
        Model.link = name + "/"

    @staticmethod
    def set_hyperparameters(population_size, matches, smr, delta):
        Model.population_size = math.floor(population_size)
        Model.matches = math.floor(matches)
        Model.starting_mutation_rate = smr
        Model.mutation_delta = delta
        time_for_final_evaluation = Model.time_per_battle * population_size * 50 + 10 * 200 * Model.time_per_battle
        time_for_evolution = Model.evolution_time - time_for_final_evaluation
        time_per_generation = population_size * matches * Model.time_per_battle
        Model.num_generations = math.floor(time_for_evolution / time_per_generation)
        if Model.population_size < 1 or Model.matches < 1 or Model.starting_mutation_rate < 0 or Model.starting_mutation_rate + Model.mutation_delta * Model.num_generations < 0:
            raise ValueError("Bad hyperparameter!")
