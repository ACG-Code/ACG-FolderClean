from tm1py_config_connect import connect_to_standard_objects

tm1 = connect_to_standard_objects()
names = tm1.dimensions.get_all_names()

mostNames = 0
subsetNames = []
mostSubsets = []
dimMostSubsets = ''

for dimName in names:
    subsetNames = tm1.subsets.get_all_names(
        dimension_name=dimName,
        hierarchy_name=None,
        private=False
    )

    if len(subsetNames) > mostNames:
        dimMostSubsets = dimName
        mostNames = len(subsetNames)
        mostSubsets = subsetNames

print("\n" + dimMostSubsets + " has the most subsets:")

for name in mostSubsets:
    print(name)