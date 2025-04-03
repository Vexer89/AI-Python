from itertools import product
from library.stripsProblem import Strips, STRIPS_domain, Planning_problem, boolean

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
                               facility_is_built('supply_depot'): location2,
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

#========================================barracks=============================================
domain_build_barracks, initial_state_build_barrcks = create_starcraft_domain(['scv'],
                                                ['sectorA', 'sectorB'],
                                                ['mineralFieldA', 'mineralFieldB'])

build_barracks_goal = {facility_is_built('barracks'): 'sectorA'}

problem_build_barracks = Planning_problem(domain_build_barracks, initial_state_build_barrcks, build_barracks_goal)
#========================================marine===============================================
domain_train_marine, initial_state_train_marine = create_starcraft_domain(['scv'],
                                        ['sectorA', 'sectorB'],
                                        ['mineralFieldA', 'mineralFieldB', 'mineralFieldC'])

marine_goal = {is_unit_trained('marine') : True}

problem_train_marine = Planning_problem(domain_train_marine, initial_state_train_marine, marine_goal)

marine_subgoal1 = {facility_is_built('supply_depot') : 'sectorA'}
marine_subgoal2 = {facility_is_built('barracks') : 'sectorB'}

problem_train_marine_subgoals = [marine_subgoal1, marine_subgoal2, marine_goal]
#===========================================tank===============================================
domain_train_tank, initial_state_train_tank = create_starcraft_domain(['scv'],
                                    ['sectorA', 'sectorB', 'sectorC'],
                                    ['mineralFieldA', 'mineralFieldB', 'mineralFieldC', 'mineralFieldD'])

tank_goal = {is_unit_trained('tank'): True}

problem_train_tank = Planning_problem(domain_train_tank, initial_state_train_tank, tank_goal)

tank_subgoal1 = {facility_is_built('supply_depot') : 'sectorA'}
tank_subgoal2 = {facility_is_built('factory') : 'sectorB'}

problem_train_tank_subgoals = [tank_subgoal1, tank_subgoal2, tank_goal]
#===========================================fusion_core=========================================

domain_build_fusion_core, initial_state_build_fusion_core = create_starcraft_domain(['scv'],
                                                   ['sectorA', 'sectorB', 'sectorC', 'sectorD', 'sectorE'],
                                                   ['mineralFieldA', 'mineralFieldB', 'mineralFieldC', 'mineralFieldD', 'mineralFieldE'])

goal_fusion_core = {facility_is_built('fusion_core'): 'sectorA'}

fusion_core_subgoal1 = {facility_is_built('supply_depot'): True}
fusion_core_subgoal2 = {facility_is_built('barracks'): True}
fusion_corer_subgoal3 = {facility_is_built('factory'): True}
fusion_core_subgoal4 = {facility_is_built('starport'): True}

problem_build_fusion_core = Planning_problem(domain_build_fusion_core, initial_state_build_fusion_core, goal_fusion_core)
problem_build_fusion_core_subgoals = [fusion_core_subgoal1, fusion_core_subgoal2, fusion_corer_subgoal3, fusion_core_subgoal4, goal_fusion_core]
#============================================Wraith=============================================

domain_train_wraith, initial_state_train_wraith = create_starcraft_domain(['scv'],
                                                    ['sectorA', 'sectorB', 'sectorC', 'sectorD'],
                                                    ['mineralFieldA', 'mineralFieldB', 'mineralFieldC', 'mineralFieldD', 'mineralFieldE'],)

wraith_goal = {is_unit_trained('wraith'): True}

problem_train_wraith = Planning_problem(domain_train_wraith, initial_state_train_wraith, wraith_goal)

wraith_subgoal1 = {facility_is_built('barracks'): True}
wraith_subgoal2 = {facility_is_built('factory'): True}
wraith_subgoal3 = {facility_is_built('starport'): True}

problem_train_wraith_subgoals = [wraith_subgoal1, wraith_subgoal2, wraith_subgoal3, wraith_goal]
#============================================BattleCruiser=============================================

domain_train_battlecruiser, initial_state_train_battlecruiser = create_starcraft_domain(['scv'],
                                                    ['sectorA', 'sectorB', 'sectorC', 'sectorD', 'sectorE'],
                                                    ['mineralFieldA', 'mineralFieldB', 'mineralFieldC', 'mineralFieldD', 'mineralFieldE', 'mineralFieldF'],)

battlecruiser_goal = {is_unit_trained('battlecruiser'): True}
battlecruiser_goal_with_subgoals = {is_unit_trained('battlecruiser'): True,
                             facility_is_built('starport'): 'secto rA',
                             facility_is_built('factory') : 'sectorC'}

battlecruiser_subgoal1 = {facility_is_built('supply_depot'): True}
battlecruiser_subgoal2 = {facility_is_built('barracks'): True}
battlecruiser_subgoal3 = {facility_is_built('factory'): True}
battlecruiser_subgoal4 = {facility_is_built('starport'): True}
battlecruiser_subgoal5 = {facility_is_built('fusion_core'): True}

problem_train_battlecruiser = Planning_problem(domain_train_wraith, initial_state_train_wraith, wraith_goal)
problem_train_battlecruiser_subgoals = [battlecruiser_subgoal1, battlecruiser_subgoal2, battlecruiser_subgoal3, battlecruiser_subgoal4, battlecruiser_subgoal5, battlecruiser_goal]
#============================================Problems=============================================
problems = { 'build barracks': problem_build_barracks,
             'train marine': problem_train_marine,
             'train tank' : problem_train_tank,
             'train wraith' : problem_train_wraith,
             'build fusion_core': problem_build_fusion_core,
             'train battlecruiser': problem_train_battlecruiser}

problems_with_subgoals = [
    {
        'name': 'train_marine_with_subgoals',
        'domain': domain_train_marine,
        'initial_state': initial_state_train_marine,
        'subgoals': problem_train_marine_subgoals
    },
    {
        'name': 'train_tank_with_subgoals',
        'domain': domain_train_tank,
        'initial_state': initial_state_train_tank,
        'subgoals': problem_train_tank_subgoals
    },
    {
        'name': 'train_wraith_with_subgoals',
        'domain': domain_train_wraith,
        'initial_state': initial_state_train_wraith,
        'subgoals': problem_train_wraith_subgoals
    }
]

hard_problems_with_subgoals = [
{
        'name': 'train_battlecruiser_with_subgoals',
        'domain': domain_train_battlecruiser,
        'initial_state': initial_state_train_battlecruiser,
        'subgoals': problem_train_battlecruiser_subgoals
    },
    {
        'name': 'build_fusion_core_with_subgoals',
        'domain': domain_build_fusion_core,
        'initial_state': initial_state_build_fusion_core,
        'subgoals': problem_build_fusion_core_subgoals
    }
]




# problems_with_subgoals = {
#              'train marine': problem_train_marine_with_subgoals,
#              'train tank' : problem_train_tank_with_subgoals,
#              'train wraith' : problem_train_wraith_with_subgoals,
#              'build fusion_core': problem_build_fusion_core_with_subgoals,
#              'train battlecruiser': problem_train_battlecruiser_with_subgoals}

# hard_problems_with_subgoals = {
#     'train battlecruiser': problem_train_battlecruiser_with_subgoals,
#     'build fusion core': problem_build_fusion_core_with_subgoals
# }