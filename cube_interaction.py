import random
from tm1py_config_connect import connect_to_standard_objects

tm1 = connect_to_standard_objects()

# Cube names
skipControlCubes = True
allCubeNames = tm1.cubes.get_all_names(not skipControlCubes)
systemCubeNames = tm1.cubes.get_all_names(skipControlCubes)

print('Printing all cubes:')
for name in allCubeNames:
    print(name)

print('Printing all cubes excluding control cubes:')
for name in systemCubeNames:
    print(name)

randomIndex = random.randrange(0, len(systemCubeNames))
cubeName = systemCubeNames[randomIndex]
cube = tm1.cubes.get(cubeName)

# For dims could use tm1.dimensions.get_all for classes instead of strings
dimensions = cube.dimensions
views = tm1.views.get_all_names(cubeName)

print('Printing dimensions of ' + cubeName)
for dimension in dimensions:
    print(dimension)

print('Printing views of ' + cubeName)
for view in views:
    print(view)