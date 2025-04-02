import STRIPS

domain = STRIPS.create_starcraft_domain(['scv'], ['areaA', 'areaB'], ['mineralA', 'mineralB'])

print(domain.feature_domain_dict)
print(domain.actions)