from sensitivity_analysis.nodes_and_edges import Edge, File
from sensitivity_analysis.constructions import ConstructionToProduct
from sensitivity_analysis.generator import calculate_impacts, find_building_sum, find_product_name
from serde.json import to_json


def calc_sensitivity(base_value: float | int, new_value: float | int, base_impact: float, new_impact: float):
    """
    Calculates a normalized sensitivity coefficient following the book " Life Cycle Assessment - Theory and Practice"
    by Hauschild, Rosenbaum and Irving Olsen, 2018, page 1083.

    :param base_value: The pase value for the specific parameter
    :param new_value: The perturbed value for the specific parameter
    :param base_impact: The base impact calculated without any perturbation
    :param new_impact: The new impact calculated with the perturbed parameter
    :return: The normalized sensitivity coefficient. According to Hauschild et al., 2018. The results show medium
             sensitivity when coefficient > 0.3, and high sensitivity when coefficient > 0.5
    """

    assert base_impact != new_value

    # Partial results calculates for better understanding
    delta_impact = abs(new_impact - base_impact)
    fraction_impact = delta_impact / base_impact

    delta_value = abs(new_value - base_value)
    fraction_value = delta_value / base_value

    sensitivity_coefficient = fraction_impact / fraction_value

    return sensitivity_coefficient


def sensitivity_of_file(data: File, initial_impact: float, perturbation: float = 0.1):
    """
    This function is made specifically to conduct sensitivity, when perturbing the product amounts.
    These amounts are found in the ConstructionToProduct edges. Therefore, this function should be expanded if
    wanting to test other parameters than product amounts.

    :param data: The specific LCAbyg data as objects. File contains Construction nodes and ConstructionToProduct edges.
    :param initial_impact: The base impact calculated before any perturbations are made
    :param perturbation: The fraction to perturb the value with. Normally 10%, so 0.1.
    :return: Several lists with the stored data, from the different analyses
    """
    # make a copy of the data to avoid overwriting the data
    data_copy = data.copy()

    # Lists for storing the needed data
    store_sensitivity_coefficients = []
    stor_product_names = []

    # Now this loop is looking specifically for ConstructionToProduct edges
    for instance in data_copy:
        if isinstance(instance, Edge):
            if isinstance(instance.edge[0], ConstructionToProduct):

                # The specific product amount is perturbed and assigned in order to make a new LCIA calculation
                initial_value, instance_id, perturbed_value = perturbation_of_value(instance, perturbation)

                # Serialize data in order to make a calculation
                data_json = to_json(data_copy)
                print(f'Initial impact: {initial_impact}')

                # Data is posted to the LCAbyg web API and impacts are calculated
                print(f'Calculate new impact...')
                results = calculate_impacts(data_json)

                # The impact is found in the result data and stored
                building_sum = find_building_sum(results)

                # Print an overview of the sensitivity analysis
                product_name = find_product_name(results, instance_id)
                stor_product_names.append(product_name)
                print(f'Perturbation of product: {product_name}')
                print(f'Amount changed from {initial_value} to {perturbed_value}')
                print(f'This perturbations results in new impact of {building_sum}')

                # calculate sensitivity coefficient
                sensitivity_coefficient = calc_sensitivity(initial_value, perturbed_value, initial_impact, building_sum)
                store_sensitivity_coefficients.append(sensitivity_coefficient)
                sensitivity_level = how_sensitive(sensitivity_coefficient)
                print(f'Sensitivity coefficient is {sensitivity_coefficient}, which means:')
                print(f'Building impact has a {sensitivity_level} sensitivity to this perturbation\n')

    return store_sensitivity_coefficients, stor_product_names


def perturbation_of_value(edge: Edge, perturbation: float):
    """
    Perturbs the value and extracts the needed information for communication of the sensitivity analysis

    :param edge: The ConstructionToProduct edge, with the product amount
    :param perturbation: The fraction, which is the percentage, to perturb the amount.
    :return: ID of the product, the unperturbed value and the perturbed value.
    """
    initial_value = edge.edge[0].amount
    instance_id = edge.edge[-1]

    varied_value = edge.edge[0].amount * perturbation
    edge.edge[0].amount = varied_value

    return initial_value, instance_id, varied_value


def how_sensitive(sens_coeff: float):
    """
    This function translates the sensitivity coefficient into one of four groups.
    The thresholds are inspired by the book " Life Cycle Assessment - Theory and Practice"
    by Hauschild, Rosenbaum and Irving Olsen, 2018, page 1083.

    :param sens_coeff: The sensitivity coefficient
    :return: A string with the level of sensitivity
    """
    sens_coeff = abs(sens_coeff)
    sensitivity_level = 'low'
    if sens_coeff >= 0.3 and sens_coeff < 0.5:
        sensitivity_level = 'medium'
    elif sens_coeff >= 0.5 and sens_coeff < 1.0:
        sensitivity_level = 'high'
    elif sens_coeff >= 1.0:
        sensitivity_level = 'very high'

    return sensitivity_level


def how_sensitive_plural(coefficients: list):
    """
    Function to assess the level of sensitivity for a list of sensitivity coefficients
    :param coefficients: list of sensitivity coefficients
    :return: list of strings with the level of sensitivity
    """
    store = []

    for coefficient in coefficients:
        store.append(how_sensitive(coefficient))

    return store
