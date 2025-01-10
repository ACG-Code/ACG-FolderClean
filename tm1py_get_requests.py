import sys
import json
import requests
from os import path
from tm1py_config_connect import connect_to_standard_objects

tm1 = connect_to_standard_objects()
url = "https://open.er-api.com/v6/latest/EUR"
processName = 'DataLoad_[ FX Rates ]_from_CSV'
process = tm1.processes.get(processName)
headers = {'Content-Type': 'text/plain', 'Content-Length': '0', 'Connection': 'keep-alive', 'User-Agent' : 'vincent-user'}
cube = tm1.cubes.get('ACG-STD-Fx Rates')
dimension = tm1.dimensions.get('ACG-STD-FxMeasure')

# Get request on the data
response = requests.get(url = url, headers=headers)
responseString = response.text
responseDict = json.loads(responseString)
baseCode = responseDict['base_code']
conversions = responseDict['rates']
cellSet = {}
usd = conversions['USD']
print(tm1.configuration)

# Convert euro conversions to dollar conversions
csvFileString = ''
for conversion in conversions:
    conversions[conversion] /= conversions['USD']
    conversionString = '%s' % conversion
    cellSet[('Actuals', 'M202402', conversionString, 'Month End')] = conversions[conversion]

print(csvFileString)

# Create the datasource on the server
dataDirectory = tm1.server.get_data_directory()
csvName = 'exchange_rates_vc.csv'
csvPath = path.join(dataDirectory, csvName)
print('Status from update...')

filenames = tm1.files.get_all_names()
for filename in filenames:
    print(filename)

# Set the datasource of the process and run it
processParameters = {'pScenario' : 'Actuals', 'pPeriod' : 'M202402'}
process.datasource_ascii_header_records = 0
process.datasource_type = 'ASCII'
process.datasource_data_source_name_for_client = csvPath
process.datasource_data_source_name_for_server = csvPath
errors = tm1.processes.compile_process(process)

print('Printing compile errors..')
if len(errors) == 0:
    print('No compile errors.')

for error in errors:
    print(error)

(statusFromProcess, statusResult, errorFile) = tm1.processes.execute_process_with_return(process = process, **processParameters)
print('Status from process execution...')
print((statusFromProcess, statusResult, errorFile))

if not statusFromProcess:
    print(tm1.processes.get_error_log_file_content(errorFile))

# Direct load a dictionary into TM1
response = tm1.cubes.cells.write_values('ACG-STD-FX Rates Copy', cellset_as_dict = cellSet)
print('Response of write values was ')
print(response)

