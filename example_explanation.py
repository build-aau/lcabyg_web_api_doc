import os
import json
import sys
from uuid import UUID
from typing import Optional, Dict, Tuple, Any, List
import requests
import base64
import time

SERVER_URL = 'https://api1.lcabyg.dk'
USERNAME = 'INSERT YOUR USERNAME'
API_KEY = 'INSERT YOUR API KEY'

TARGET = 'lcabyg5+br23'
OUTPUT_PATH = 'results.json'

# EXAMPLE sending a job containing multiple projects:
PROJECT_PATHS = ['testdata/lcabyg/single/', 'testdata/lcabyg/reno', 'testdata/lcabyg/empty']

""" ABOUT example_explanation.py:
This example file gives a detailed run-through of the connecting, logging, and sending/receiving job into the API WITHOUT the packages sbi_web_api_py and lcabyg_web_api_py. 

Get started by creating a user account at https://api.lcabyg.dk/da/
Place the user name and api key in the fields "USERNAME" and "API_KEY" located in the function example_send_job().

The function example_send_job() shows examples of each step of interacting with the API. 
The function example_debug_job_data provides an example for debugging errors in the job_data sent to the API. We always recommend reading the LCAbyg JSON Guide prior to working with LCAbyg JSON.  

NOTICE: the API_KEY is not the same as the TOKEN.
NOTICE: The functions get(), post(), put(), and delete() should NOT be modified. They are the essential functions for talking to the API.
NOTICE: It is important to indicate when you have finished talking to the API. The queue limit will fill if you have yet to cancel your calls. See the function mark_job_as_finished. 
NOTICE: When the job is marked as finished, your job will be removed from the system sooner or later. It can only be done one time per job.

"""


class AuthTokenExpired(Exception):
    def __init__(self, res: requests.Response):
        self.response = res


def login_via_headers(server_url: str, username: str, password: str) -> str:
    """
    Use TOKEN for all calls where security is involved.
    Create a user account at https://api.lcabyg.dk/da/

    NOTICE: Login can be done using other methods. Read more in the section "Login", in api.md.

    :param server_url:
    :param username:
    :param password:
    :return: TOKEN
    """
    res = post(f'{server_url}/v2/login', auth=(username, password))

    UUID(res)
    # In this case, res should be a string and not UUID
    return res


def ping(server_url: str) -> str:
    """
    Check server connection WITHOUT login.
    If connection, the response is 'pong'.

    :param server_url:
    :return: 'pong'
    """
    return get(f'{server_url}/v2/ping')


def ping_secure(server_url: str, auth_token: str) -> str:
    """
    Check server connection WITH login.
    If connection, the response is 'pong_secure'.

    :param server_url:
    :param auth_token: Generated from login_via_headers(SERVER_URL, USERNAME, API_KEY)
    :return: 'pong_secure'
    """
    return get(f'{server_url}/v2/ping_secure', auth_token=auth_token)


def collect_json(json_paths: List[str]) -> List[Dict[str, Any]]:
    """
    The API requires the job_data to contain one json file per project.
    Secrets.json is immutable Gen_DK data.

    :param json_paths: One path per json project
    :return: One combined json file for the json project of the given project path
    """

    assert isinstance(json_paths, list)
    collected_projects = list()

    # Project paths is a list of project paths. For each path:
    for start_path in json_paths:
        # Makes sure the base path is the user's home directory
        start_path = os.path.expanduser(start_path)
        # If the path is an existing directory
        if os.path.isdir(start_path):
            # Goes through everything in the directory of the project path
            for root, directories, files in os.walk(start_path):
                for file in files:
                    target_path = os.path.join(root, file)
                    # If the file extension is ".json", then combine into one json file which Python can understand (Converts JSON to the datatype Dict)
                    if os.path.isfile(target_path) and os.path.splitext(target_path)[1].lower() == '.json':
                        with open(target_path, 'r', encoding='utf-8') as f:
                            collected_project = json.load(f)
                        assert isinstance(collected_project, list)
                        collected_projects.extend(collected_project)
        # If the path is one json file
        else:
            with open(start_path, 'r', encoding='utf-8') as f:
                collected_project = json.load(f)
            assert isinstance(collected_project, list)
            collected_projects.extend(collected_project)

    return collected_projects


def create_job_data(target: str, collected_projects: list) -> Dict:
    """
    As the scope of underlying software architecture is broader than LCAbyg Web API, the system must be able to handle other data types than JSON.
    This makes it necessary to encode and decode the JSON data.

    This function describe the processes for creating the job data. This includes encoding/decoding json TO the API (packing bytes). Read more here: https://en.wikipedia.org/wiki/Base64
    See the function unpack_bytes for decoding data from the API.

    :param target:
    :param collected_projects: JSON files collected and converted to the datatype Dict)
    :return: job_data (json data that the API can understand)
    """

    # Datatype: dict converted from json
    input_dict = collect_json(collected_projects)

    # Datatype: string converted from dict
    input_string = json.dumps(input_dict)

    # Datatype: bytes converted from string
    input_bytes = input_string.encode('utf-8')

    # Datatype: string base 64 converted from bytes (encoding) (https://en.wikipedia.org/wiki/Base64)
    input_string_base64 = base64.standard_b64encode(input_bytes).decode('utf-8')

    job_data = {
        'priority': 0,
        'job_target': target,
        'job_target_min_ver': '',
        'job_target_max_ver': '',
        'job_arguments': '',
        'extra_input': '',
        'input_blob': input_string_base64,
        'input_data': collect_json(collected_projects)
    }

    return job_data


def unpack_bytes(data):
    """
    This function unpack_bytes for decoding data from the API.
    See the function create_job_data for packing bytes and creating data for the API.

    :param data:
    :return: decoded data (json data that Python can understand)
    """

    decode_data = base64.standard_b64decode(data)
    bytes_to_string = decode_data.decode('utf-8')
    string_to_dict = json.loads(bytes_to_string)

    return string_to_dict


def get_job_ids(server_url: str, auth_token: str) -> str:
    """
    Gives all job ids on the account you are logged in with.

    :param server_url:
    :param auth_token:
    :return: List of job ids (UUIDs converted to strings)
    """
    return get(f'{server_url}/v2/jobs', auth_token=auth_token)


def get_job_by_id(server_url: str, job_id: str, auth_token: str) -> str:
    """
    :param server_url:
    :param job_id: UUIDs converted to strings. See the function get_job_ids
    :param auth_token:
    :return: List of dictionaries for the jobs in the account. Each dictionary contains information on the specific job.
    """

    return get(f'{server_url}/v2/jobs/{job_id}', auth_token=auth_token)


def post_job(server_url: str, body: dict, auth_token: str) -> str:
    """

    :param server_url:
    :param body: The json data you want to send.
    :param auth_token:
    :return: output data. Error_messages are found in 'extra_output'
    """
    return post(f'{server_url}/v2/jobs', body, auth_token=auth_token)


def get_job_input_by_id(server_url: str, job_id: str, auth_token: str):
    """
    The return data needs to be decoded for Python to understand the data. See an example of this in the function unpack_bytes.

    :param server_url:
    :param job_id:
    :param auth_token:
    :return: input model.json.
    """
    return get(f'{server_url}/v2/jobs/{job_id}/input', auth_token=auth_token)


def get_job_output_by_id(server_url, job_id: str, auth_token: str):
    """
    The return data needs to be decoded for Python to understand the data. See an example of this in the function unpack_bytes.

    A three-layer hierarchy structures the results:

    1. Instance id corresponding to ids in the model
    2. Stage/aggregation approach (for instance, SUM)
    3. Year - please note that year 9999 represents the total sum of all years.

    Read the LCAbyg JSON guide for more info.

    :param server_url:
    :param job_id:
    :param auth_token:
    :return: results and input model.json.
    """
    return get(f'{server_url}/v2/jobs/{job_id}/output', auth_token=auth_token)


def mark_job_as_finished(server_url: str, job_id: str, auth_token: str):
    """
    Finally, you should mark the job as finished when you have all the data you need.
    It is important to indicate when you have finished talking to the API. If you have not canceled your calls, the queue limit will fill. See the function mark_job_as_finished.

    NOTICE: It can only be done one time per job.

    :param server_url:
    :param job_id:
    :param auth_token:
    :return: Please be aware that when the job is marked as finished, your job will be removed from the system sooner or later.
    """
    return delete(f'{server_url}/v2/jobs/{job_id}', auth_token=auth_token)


def get(url: str,
        headers: Optional[Dict] = None,
        auth_token: Optional[str] = None) -> Any:
    """
    NOTICE: The functions get(), post(), put(), and delete() should NOT be modified. They are the essential functions for talking to the API.
    :param url:
    :param headers:
    :param auth_token:
    :return:
    """
    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'GET ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def post(url: str,
         data: Optional[Dict] = None,
         headers: Optional[Dict] = None,
         auth_token: Optional[str] = None,
         auth: Optional[Tuple[str, str]] = None) -> Any:
    """
    NOTICE: The functions get(), post(), put(), and delete() should NOT be modified. They are the essential functions for talking to the API.
    :param url:
    :param data:
    :param headers:
    :param auth_token:
    :param auth:
    :return:
    """
    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.post(url, json=data, headers=headers, auth=auth)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'POST ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def put(url: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        auth_token: Optional[str] = None,
        auth: Optional[Tuple[str, str]] = None) -> Any:
    """
    NOTICE: The functions get(), post(), put(), and delete() should NOT be modified. They are the essential functions for talking to the API.
    :param url:
    :param data:
    :param headers:
    :param auth_token:
    :param auth:
    :return:
    """
    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.put(url, json=data, headers=headers, auth=auth)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'PUT ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def delete(url: str,
           headers: Optional[Dict] = None,
           auth_token: Optional[str] = None) -> Any:
    """
    NOTICE: The functions get(), post(), put(), and delete() should NOT be modified. They are the essential functions for talking to the API.
    :param url:
    :param headers:
    :param auth_token:
    :return:
    """
    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'DELETE ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def example_send_job(server_url, token, target, output_path, project_paths):
    # Notice:  list of paths
    for project_path in project_paths:

        print('Connecting to the server:')
        res_ping = ping(server_url)
        print(f'res_ping = {res_ping}. You are  connected to the server!\n')

        print('Connecting to the server and logging in:')
        res_ping_secure = ping_secure(server_url, auth_token=token)
        print(f'res_ping = {res_ping_secure}. You are connected to the server and logged in!\n')

        print('Create job data from list of paths:')
        res_job_data = create_job_data(target, [project_path])
        print('The json data has created!\n')

        print('\Post job:')
        res_post_job = post_job(server_url, body=res_job_data, auth_token=token)
        print(f"Job posted! Status: {res_post_job}\n")

        print('Waiting for the job to finish:')
        not_done = True
        while not_done:
            status = res_post_job['status']
            print(f'status = {status}')
            not_done = (status == 'New') or (status == 'Started')
            time.sleep(1)
            res_post_job = get_job_by_id(server_url, job_id=res_post_job['id'], auth_token=token)
            print(f"The information for job id: {res_post_job['id']} is: {res_post_job}\n")
            print()
        print(f'Done: status = {status}')

        print('Get job input (model) by job id:')
        res_get_job_input_by_id = get_job_input_by_id(server_url, job_id=res_post_job['id'], auth_token=token)
        decode_res_get_job_input_by_id = unpack_bytes(res_get_job_input_by_id)
        print(f"The job input for job id: {res_post_job['id']} is: {decode_res_get_job_input_by_id}\n")

        print('Download the results:')
        res_get_job_output_by_id = get_job_output_by_id(server_url, job_id=res_post_job['id'], auth_token=token)
        decode_res_get_job_output_by_id = unpack_bytes(data=res_get_job_output_by_id)
        print(f"The LCA results for job id {res_post_job['id']} are: {decode_res_get_job_output_by_id}\n")

        # This can only be done one time per job:
        print('Mark job as finished:')
        # res_mark_job_as_finished = mark_job_as_finished(SERVER_URL, job_id=example_job_id, auth_token=TOKEN)
        print('Job is marked as finished:\n')

        print('Saving the results to disk:')
        # data = json.loads(decode_res_get_job_output_by_id)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(decode_res_get_job_output_by_id, f, indent=2, ensure_ascii=False)
        print()


def example_debug_job_data(server_url, token, project_path):
    """
    Running this function will give the Traceback error: "json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
    A more detailed explanation.

    :param server_url:
    :param token:
    :param target:
    :param project_path:
    :return:
    """
    # Collection and encoding job data with errors
    res_job_data = create_job_data(TARGET, project_path)

    # Post the job
    res_post_job_error = post_job(server_url, body=res_job_data, auth_token=token)

    print('Waiting for the job to finish:')
    not_done = True
    while not_done:
        status = res_post_job_error['status']
        print(f'status = {status}')
        not_done = (status == 'New') or (status == 'Started')
        time.sleep(1)
        res_post_job_error = get_job_by_id(server_url, job_id=res_post_job_error['id'], auth_token=token)
        print(f"The information for job id: {res_post_job_error['id']} is: {res_post_job_error}")
        print()
    print(f'Done: status = {status}')

    if status == 'Failed':
        print(
            f"\nLog error causing the job id {res_post_job_error['id']} to fail: \n{res_post_job_error['extra_output']}\n")
    else:
        print('Get job input (model) by job id:')
        res_get_job_input_by_id = get_job_input_by_id(server_url, job_id=res_post_job_error['id'], auth_token=token)
        decode_res_get_job_input_by_id = unpack_bytes(res_get_job_input_by_id)
        print(f"The job input for job id: {res_post_job_error['id']} is: {decode_res_get_job_input_by_id}\n")

        print('Download the results:')
        res_get_job_output_by_id = get_job_output_by_id(server_url, job_id=res_post_job_error['id'], auth_token=token)
        decode_res_get_job_output_by_id = unpack_bytes(data=res_get_job_output_by_id)
        print(f"The LCA results for job id {res_post_job_error['id']} are: {decode_res_get_job_output_by_id}\n")

        # This can only be done one time per job:
        print('Mark job as finished:')
        # res_mark_job_as_finished = mark_job_as_finished(SERVER_URL, job_id=example_job_id, auth_token=TOKEN)
        print('Job is marked as finished:\n')


def main():
    # Create a user account  and get a API_KEY at https://api.lcabyg.dk/da/
    token = login_via_headers(SERVER_URL, USERNAME, API_KEY)

    example_send_job(SERVER_URL, token, TARGET, OUTPUT_PATH, PROJECT_PATHS)

    # EXAMPLE sending a job containing one projects with one error in Building.json:
    # project_path_with_error = ['testdata/lcabyg/single_with_error']
    # example_debug_job_data(SERVER_URL, token, project_path_with_error)


if __name__ == '__main__':
    main()
