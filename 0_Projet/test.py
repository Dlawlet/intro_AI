import copy
dico = { "a": {"b": 2, "c": [1,6]}, "b": 2, "c": 3}
cop = copy.deepcopy(dico)

dico["a"]["c"][1] = 4

print(dico)
print(cop)