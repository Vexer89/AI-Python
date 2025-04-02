# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python code Version 0.9.15 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation
from itertools import product


# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Strips(object):
    def __init__(self, name, preconds, effects, cost=1):
        """
        defines the STRIPS representation for an action:
        * name is the name of the action
        * preconds, the preconditions, is feature:value dictionary that must hold
        for the action to be carried out
        * effects is a feature:value map that this action makes
        true. The action changes the value of any feature specified
        here, and leaves other features unchanged.
        * cost is the cost of the action
        """
        self.name = name
        self.preconds = preconds
        self.effects = effects
        self.cost = cost

    def __repr__(self):
        return self.name

class STRIPS_domain(object):
    def __init__(self, feature_domain_dict, actions):
        """Problem domain
        feature_domain_dict is a feature:domain dictionary,
                mapping each feature to its domain
        actions
        """
        self.feature_domain_dict = feature_domain_dict
        self.actions = actions

class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal):
        """
        a planning problem consists of
        * a planning domain
        * the initial state
        * a goal
        """
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal

boolean = {False, True}

#b - {} area - {

# BLoc = {area}
# collected_minerals = boolean
# are_barracks_builded = boolean / is_marine_trained = boolean
# is_sector_available
#

# delivery_domain = STRIPS_domain(
#     {'RLoc':{'cs', 'off', 'lab', 'mr'}, 'RHC':boolean, 'SWC':boolean,
#      'MW':boolean, 'RHM':boolean},           #feature:values dictionary
#     { Strips('mc_cs', {'RLoc':'cs'}, {'RLoc':'off'}),
#      Strips('mc_off', {'RLoc':'off'}, {'RLoc':'lab'}),
#      Strips('mc_lab', {'RLoc':'lab'}, {'RLoc':'mr'}),
#      Strips('mc_mr', {'RLoc':'mr'}, {'RLoc':'cs'}),
#      Strips('mcc_cs', {'RLoc':'cs'}, {'RLoc':'mr'}),
#      Strips('mcc_off', {'RLoc':'off'}, {'RLoc':'cs'}),
#      Strips('mcc_lab', {'RLoc':'lab'}, {'RLoc':'off'}),
#      Strips('mcc_mr', {'RLoc':'mr'}, {'RLoc':'lab'}),
#      Strips('puc', {'RLoc':'cs', 'RHC':False}, {'RHC':True}),
#      Strips('dc', {'RLoc':'off', 'RHC':True}, {'RHC':False, 'SWC':False}),
#      Strips('pum', {'RLoc':'mr','MW':True}, {'RHM':True,'MW':False}),
#      Strips('dm', {'RLoc':'off', 'RHM':True}, {'RHM':False})
#    } )
#
# problem0 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'RLoc':'off'})
# problem1 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'SWC':False})
# problem2 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'SWC':False, 'MW':False, 'RHM':False})
#
# ### blocks world
# def move(x,y,z):
#     """string for the 'move' action"""
#     return 'move_'+x+'_from_'+y+'_to_'+z
# def on(x):
#     """string for the 'on' feature"""
#     return x+'_is_on'
# def clear(x):
#     """string for the 'clear' feature"""
#     return 'clear_'+x
# def create_blocks_world(blocks = {'a','b','c','d'}):
#     blocks_and_table = blocks | {'table'}
#     stmap =  {Strips(move(x,y,z),{on(x):y, clear(x):True, clear(z):True},
#                                  {on(x):z, clear(y):True, clear(z):False})
#                     for x in blocks
#                     for y in blocks_and_table
#                     for z in blocks
#                     if x!=y and y!=z and z!=x}
#     stmap.update({Strips(move(x,y,'table'), {on(x):y, clear(x):True},
#                                  {on(x):'table', clear(y):True})
#                     for x in blocks
#                     for y in blocks
#                     if x!=y})
#     feature_domain_dict = {on(x):blocks_and_table-{x} for x in blocks}
#     feature_domain_dict.update({clear(x):boolean for x in blocks_and_table})
#     return STRIPS_domain(feature_domain_dict, stmap)
#
# blocks1dom = create_blocks_world({'a','b','c'})
# blocks1 = Planning_problem(blocks1dom,
#      {on('a'):'table', clear('a'):True,
#       on('b'):'c',  clear('b'):True,
#       on('c'):'table', clear('c'):False}, # initial state
#      {on('a'):'b', on('c'):'a'})  #goal
#
# blocks2dom = create_blocks_world({'a','b','c','d'})
# tower4 = {clear('a'):True, on('a'):'b',
#           clear('b'):False, on('b'):'c',
#           clear('c'):False, on('c'):'d',
#           clear('d'):False, on('d'):'table'}
# blocks2 = Planning_problem(blocks2dom,
#      tower4, # initial state
#      {on('d'):'c',on('c'):'b',on('b'):'a'})  #goal
#
# blocks3 = Planning_problem(blocks2dom,
#      tower4, # initial state
#      {on('d'):'a', on('a'):'b', on('b'):'c'})  #goal



#features
def builder_location(builder):
    return f'{builder}_is_in'

def collected_minerals(builder):
    return f'{builder}_has_minerals'

def facility_is_built(facility):
    return f'{facility}_is_built'

# is buliding in {location} : boolean
def is_building(location):
    return f'is_building_in_{location}'

def is_empty(location):
    return f'{location}_is_empty'

def is_unit_trained(unit):
    return f'{unit}_is_trained'

#actions

def move(builder, location1, location2):
    return f'move_{builder}_from_{location1}_to_{location2}'

def collect_minerals(builder, location):
    return f'collect_minerals_from_{location}_by_{builder}'

def build_supply_depot(builder, location):
     return f'build_supply_depot_in_{location}_by_{builder}'

def build_barracks(builder, location1, location2):
    return f'build_barracks_in_{location1}_by_{builder}_using_{location2}'

def build_factory(builder, location1, location2):
    return f'build_factory_in_{location1}_by_{builder}_using_{location2}'

def build_starport(builder, location1, location2):
    return f'build_starport_in_{location1}_by_{builder}_using_{location2}'

def build_fusion_core(builder, location1, location2):
    return f'build_fusion_core_in_{location1}_by_{builder}_using_{location2}'

def train_marine(builder, location):
     return f"train marine in {location} by {builder}"

def train_tank(builder, location):
    return f'train tank in {location} by {builder}'

def train_wraith(builder, location):
    return f'train wraith in {location} by {builder}'

def train_battlecruiser(builder, location1, location2):
    return f'train battlecruiser in {location1} by {builder}'

starcraft_units = ('marine', 'tank', 'wraith', 'battlecruiser')
starcraft_facilities = ('supply_depot', 'barracks', 'factory', 'starport', 'fusion_core')

#domain creation
def create_starcraft_domain(builders, building_areas, minerals_areas, facilities=starcraft_facilities, units=starcraft_units):

    areas = building_areas + minerals_areas

    feature_domain_dict = {}
    initial_state = {}

    for builder in builders:
        feature_domain_dict[builder_location(builder)] = set(areas)
        feature_domain_dict[collected_minerals(builder)] = boolean

        initial_state[builder_location(builder)] = areas[0]
        initial_state[collected_minerals(builder)] = False

    for facility in facilities:
        feature_domain_dict[facility_is_built(facility)] = set(building_areas + [None])

        initial_state[facility_is_built(facility)] = None

    for location in building_areas:
        feature_domain_dict[is_building(location)] = boolean

        initial_state[is_building(location)] = False

    for location in minerals_areas:
        feature_domain_dict[is_empty(location)] = boolean

        initial_state[is_empty(location)] = False

    for unit in units:
        feature_domain_dict[is_unit_trained(unit)] = boolean

        initial_state[is_unit_trained(unit)] = False

    actions = []

    for builder, location1, location2 in product(builders, areas, areas):
        if location1 == location2:
            continue
        actions.append(Strips(move(builder, location1, location2),
                              {builder_location(builder): location1},
                              {builder_location(builder): location2}))

    for builder, location in product(builders, minerals_areas):
        actions.append(Strips(collect_minerals(builder, location),
                              {builder_location(builder): location, is_empty(location): False},
                              {is_empty(location): True, collected_minerals(builder): True}))

    for builder, location1, location2 in product(builders, building_areas, building_areas):
        if location1 == location2:
            continue
        actions.append(Strips(build_supply_depot(builder, location1),
                              {builder_location(builder): location1,
                               is_building(location1) : False,
                               collected_minerals(builder) : True},
                              {is_building(location1) : True,
                               collected_minerals(builder) : False,
                               facility_is_built('supply_depot') : location1}
                              ))

        actions.append(Strips(build_barracks(builder, location1, location2),
                              {builder_location(builder): location1,
                               facility_is_built('supply-depot'): location2,
                               collected_minerals(builder): True,
                               is_building(location1): False},
                              {is_building(location1): True,
                               collected_minerals(builder): False,
                               facility_is_built('barracks'): location1}
                              ))

        actions.append(Strips(build_factory(builder, location1, location2),
                              {builder_location(builder): location1,
                               facility_is_built('barracks'): location2,
                               collected_minerals(builder): True,
                               is_building(location1): False},
                              {is_building(location1): True,
                               collected_minerals(builder): False,
                               facility_is_built('factory'): location1}
                              ))

        actions.append(Strips(build_starport(builder, location1, location2),
                              {builder_location(builder): location1,
                               facility_is_built('factory'): location2,
                               collected_minerals(builder): True,
                               is_building(location1): False},
                              {is_building(location1): True,
                               collected_minerals(builder): False,
                               facility_is_built('starport'): location1}
                              ))

        actions.append(Strips(build_fusion_core(builder, location1, location2),
                              {builder_location(builder): location1,
                               facility_is_built('starport'): location2,
                               collected_minerals(builder): True,
                               is_building(location1): False},
                              {is_building(location1): True,
                               collected_minerals(builder): False,
                               facility_is_built('fusion_core'): location1}
                              ))

        actions.append(Strips(train_marine(builder, location1),
                              {builder_location(builder): location1,
                               facility_is_built('barracks'): location1,
                               collected_minerals(builder): True},
                              {is_unit_trained('marine'): True,
                               collected_minerals(builder): False}))

        actions.append(Strips(train_tank(builder, location1),
                              {builder_location(builder): location1,
                               facility_is_built('factory'): location1,
                               collected_minerals(builder): True},
                              {is_unit_trained('tank'): True,
                               collected_minerals(builder): False}))

        actions.append(Strips(train_wraith(builder, location1),
                              {builder_location(builder): location1,
                               facility_is_built('starport'): location1,
                               collected_minerals(builder): True},
                              {is_unit_trained('wraith'): True,
                               collected_minerals(builder): False}))

        actions.append(Strips(train_battlecruiser(builder, location1, location2),
                              {builder_location(builder): location1,
                               facility_is_built('starport'): location1,
                               facility_is_built('fusion_core'): location2,
                               collected_minerals(builder): True},
                              {is_unit_trained('battlecruiser'): True,
                               collected_minerals(builder): False}))


    return STRIPS_domain(feature_domain_dict, actions), initial_state

domain_train_marine, initial_state_train_marine = create_starcraft_domain(['scv'],
                                        ['sectorA', 'sectorB'],
                                        ['mineralFieldA', 'mineralFieldB', 'mineralFieldC'])

goal = {is_unit_trained('marine') : True}

problem_train_marine = Planning_problem(domain_train_marine, initial_state_train_marine, goal)

print(problem_train_marine.initial_state, problem_train_marine.goal)