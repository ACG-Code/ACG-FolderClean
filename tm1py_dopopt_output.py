import csv
import json
import requests
from docopt import docopt
from tm1py_config_connect import ConfigConnector as cc

usage = """
tm1py_docopt_output

Usage: 
  tm1py_docopt_output.py <scenario> <period> [-d <datasource_path>]
  tm1py_docopt_output.py (-h | --help)

Options: 
  -d             The destination for the datasource [default: /TM1_Servers/SYSTEM/StandardObjects/Data/exchange_rates_vc.csv]
  -h, --help     Display help.
"""

arguments = docopt(usage)  # parse arguments based on docstring above

scenario = arguments['<scenario>']
period = arguments['<period>']
datasource_path = arguments['<datasource_path>']

if arguments['-d']:
    print('Was provided datasource_path: ' + datasource_path)
else:
    print('Was not provided datasource_path, defaulting: ' + datasource_path)

tm1 = cc.connect_to_standard_objects()
url = "https://open.er-api.com/v6/latest/EUR"
processName = 'DataLoad_[ FX Rates ]_from_CSV'
process = tm1.processes.get(processName)
headers = {'Content-Type': 'text/plain', 'Content-Length': '0', 'Connection': 'keep-alive',
           'User-Agent': 'vincent-user'}
cube = tm1.cubes.get('ACG-STD-Fx Rates')
dimension = tm1.dimensions.get('ACG-STD-FxMeasure')

# Get request on the data
response = requests.get(url=url, headers=headers)
responseString = response.text
responseDict = json.loads(responseString)
baseCode = responseDict['base_code']
conversions = responseDict['rates']
cellSet = {}
usd = conversions['USD']
print(tm1.configuration)

print('Status from update...')

# Set the datasource of the process and run it
processParameters = {'pScenario': scenario, 'pPeriod': period}
process.datasource_ascii_header_records = 0
process.datasource_type = 'ASCII'
process.datasource_data_source_name_for_client = datasource_path
process.datasource_data_source_name_for_server = datasource_path
errors = tm1.processes.compile_process(process)

if len(errors) == 0:
    print('No compile errors.')
else:
    print('Printing compile errors..')

for error in errors:
    print(error)

(statusFromProcess, statusResult, errorFile) = tm1.processes.execute_process_with_return(process=process,
                                                                                         **processParameters)
print('Status from process execution...')
print((statusFromProcess, statusResult, errorFile))

if not statusFromProcess:
    print(tm1.processes.get_error_log_file_content(errorFile))





