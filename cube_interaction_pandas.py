import TM1py
from tm1py_config_connect import connect_to_standard_objects

viewName = 'Default'
cubeName = 'ACG-STD-FX Rates'
otherCubeName = 'ACG-STD-FX Rates Copy'
tm1 = connect_to_standard_objects()
fxRatesCube = tm1.cubes.get(cubeName)

otherCubeExists = tm1.cubes.exists(otherCubeName)

if not otherCubeExists:
    cubeDimensions = tm1.cubes.get_dimension_names(cubeName)
    otherCube = TM1py.Cube(otherCubeName, cubeDimensions)
    tm1.cubes.create(otherCube)
    print('Created copied cube ' + otherCubeName)
else:
    print('Cube already exists: ' + otherCubeName)

tm1.cells.clear(otherCubeName)

mdx = """
SELECT NON EMPTY
{TM1FILTERBYLEVEL({[ACG-STD-Scenario].[ACG-STD-Scenario].MEMBERS}, 0)} *
{TM1FILTERBYLEVEL({[ACG-STD-Time].[ACG-STD-Time].MEMBERS}, 0 )} *
{TM1FILTERBYLEVEL({[ACG-STD-Currency].[ACG-STD-Currency].MEMBERS}, 0 )} *
{TM1FILTERBYLEVEL({[ACG-STD-FxMeasure].[ACG-STD-FxMeasure].MEMBERS}, 0 )}
ON 0
FROM [ACG-STD-FX Rates]
"""

dataframe = tm1.cells.execute_mdx_dataframe(mdx)
indices = ['ACG-STD-Scenario','ACG-STD-Time', 'ACG-STD-Currency', 'ACG-STD-FxMeasure']
pivot = dataframe.pivot_table(index = indices, values = 'Value')

pivot.loc[('Actuals', 'M202401', 'CAD', 'Month AVG')] = 2.5
pivot.loc[('Actuals', 'M202401', 'USD', 'Month AVG')] = 2.5
dataframe = pivot.reset_index()

new_cell_data = {}
for row in dataframe.iterrows():
    rowVal = row[1]
    new_cell_data[(rowVal.iloc[0], rowVal.iloc[1], rowVal.iloc[2], rowVal.iloc[3])] = rowVal.iloc[4]

tm1.cubes.cells.write_values(otherCubeName, new_cell_data)