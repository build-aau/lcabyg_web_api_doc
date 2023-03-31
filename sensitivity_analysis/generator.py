import json
from uuid import UUID
from sensitivity_analysis.nodes_and_edges import File
from serde.json import from_json
import os
import time
from lcabyg_web_api_py import *


def read_json_file(path: str) -> File:
    """
    ONLY WORKS WITH THE DATA THAT FIT WITH IMPLEMENTED CLASSES -> Construction and ConstructionToProduct in Node and
    Edge in File
    Read one json file and deserialize to the objects that fit the LCAbyg json structure.
    :param path: str of path to file location
    :return: Will return a list of objects
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        return from_json(File, data)


def calculate_impacts(data: str):
    """
    The LCAbyg web API code, which posts the json project to the API.
    :param data: str with the data
    :return: The output from the API, which is the model and results as json
    """

    # Next two lines are compatible with pycharm. Otherwise, just replace os.environ.get('USERNAME') with username ect.
    USERNAME = os.environ.get('USERNAME')  # Username is the username, from the API website
    API_KEY = os.environ.get('API_KEY')  # API_KEY is the key retrieved from the API website

    cli = Client(USERNAME, API_KEY)
    cli.api_ping_test()

    # Write the json data to a file to prepare for job submission
    # When running the sensitivity this file will be overwritten for every calculation
    with open('sensitivity_analysis/testdata/wall_example/User/wall_data.json', 'w', encoding='utf-8') as f:
        json_data = json.loads(data)
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # The job is submitted
    job, output_blob = cli.submit_job(NewJob(project=collect_json(['sensitivity_analysis/testdata/wall_example/'])))
    return output_blob


def find_building_sum(result_data: dict):
    """
    Helper function to get the GWP result/impact for the full building
    :param result_data: The API result output
    :return: a float with the result
    """
    building_id = ''

    assert 'model' in result_data
    for instance in result_data['model']:
        assert 'node_type' in instance
        if instance['node_type'] == 'Building':
            building_id = instance['id']

    assert 'results' in result_data
    result = result_data['results'][building_id]['Sum']['9999']['GWP']

    return result


def find_product_name(result_data: dict, product_id: UUID):
    """
    Helper function to find the name for a product, from its id.
    :param result_data: The API result output
    :param product_id: The uuid of the product - the model id
    :return: str with product name
    """
    assert 'model' in result_data
    for instance in result_data['model']:
        assert 'node_type' in instance
        if instance['node_type'] == 'ProductInstance':
            if instance['model_id'] == product_id:
                assert 'Danish' in instance['name']
                product_name = instance['name']['Danish']
                return product_name
