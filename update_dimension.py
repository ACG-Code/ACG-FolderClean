import TM1py
from tm1py_config_connect import connect_to_standard_objects, connect_to_blank_training

# Add the element
dimName = 'Clients'
elementName = 'Vincent Cinardo'
elementType = 'NUMERIC'
element = TM1py.Element(elementName, elementType)
stdObjectsTM1 = connect_to_standard_objects()

elementExists = stdObjectsTM1.elements.exists(dimName, dimName, elementName)

if not elementExists:
    stdObjectsTM1.elements.create(dimName, dimName, element)
    print('Added element ' + elementName)
else:
    print(elementName + ' already exists in ' + dimName)

# Copy the dimension to another instance
dimension = stdObjectsTM1.dimensions.get(dimName)
blankTrainingTM1 = connect_to_blank_training()
dimExists = blankTrainingTM1.dimensions.exists(dimName)

if dimExists:
    print(dimName + ' existed; updating.')
else:
    print(dimName + ' does not exist; creating.')

blankTrainingTM1.dimensions.update_or_create(dimension)