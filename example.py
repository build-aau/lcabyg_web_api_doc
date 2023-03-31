import os
from lcabyg_web_api_py import *

"""
This example uses the libraries lcabyg_web_api_py and sbi_web_api.py connecting, logging, and sending/receiving job into the LCAbyg Web API. 
See raw_api.py in the package / folder sbi_web_api.py for source code.

Get started by creating a user account at https://api.lcabyg.dk/da/
Place the user name and api key in the fields "USERNAME" and "API_KEY" located in the function example_send_job().
"""

# Turn this on if not using environment variables
USERNAME = 'INSERT YOUR USERNAME'
API_KEY = 'INSERT YOUR API KEY'

# Turn this on if using environment variables
#USERNAME = os.environ.get('INSERT YOUR USERNAME')
#API_KEY = os.environ.get('INSERT YOUR API API_KEY')

if not USERNAME or not API_KEY:
    print('Please provide a USERNAME, API_KEY')
    exit(1)

cli = Client(USERNAME, API_KEY)

for project_path in ['testdata/lcabyg/empty/', 'testdata/lcabyg/reno/', 'testdata/lcabyg/single/']:
    data = NewJob(project=collect_json([project_path]))
    job, output = cli.submit_job(data)
    print(f'{project_path}: {job.status}')
    print(output)
    print()