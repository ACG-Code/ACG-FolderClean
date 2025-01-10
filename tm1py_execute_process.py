from tm1py_config_connect import connect_to_standard_objects

tm1 = connect_to_standard_objects()
names = tm1.processes.get_all_names()
process = tm1.processes.get('DataLoad_[ FX Rates ]_from_CSV')
parameters = {
    'pScenario' : 'Actuals',
    'pPeriod' : 'M202402',
}
tm1RVal = tm1.processes.execute_process_with_return(
    process,
    timeout = None,
    cancel_at_timeout=True,
    **parameters
)

print(tm1RVal)