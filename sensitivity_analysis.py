import os
from serde.json import to_json
from sensitivity_analysis.generator import read_json_file, calculate_impacts, find_building_sum
from sensitivity_analysis.sensitivity import sensitivity_of_file, how_sensitive_plural
from sensitivity_analysis.visualize import bar_plot


# Turn this on if not using environment variables
USERNAME = 'INSERT YOUR USERNAME'
API_KEY = 'INSERT YOUR API KEY'

# Save username and password as environment variables
os.environ['USERNAME'] = USERNAME
os.environ['API_KEY'] = API_KEY


def main():
    """
    This example aims to show how the LCAbyg web API can be used to conduct a sensitivity analysis.
    The analysis is made on an example of a wall, where only the product (byggevare) amounts are perturbed.
    This could be expanded to other parameters, which will require some adaption of the sensitivity code.
    The sensitivity calculations are only made for GWP, which can be expanded to other impact categories.

    Sensitivity tells whether LCIA results (impacts) are sensitive to perturbation in specific parameters.
    This can help in the iterative LCA process to only focus on detailing " important " parameters.
    
    Disclaimer: The code is a simple example, part of a bigger project (WIP). It is not optimized, so
                suggestions for changes will be appreciated.

    :return: Prints the info from sensitivity analyses as they happen and visualized in a bar plot at the end
    """
    # This wall is an example of an element with three constructions (interior alkyd paint w. full plastering,
    # wood construction w. mineral wool and exterior bricks)

    data_path = 'sensitivity_analysis/testdata/wall.json'

    # Get the initial data as objects, see constructions.py:
    data_obj = read_json_file(data_path)

    # Calculate the base case without perturbation to get the base impacts, needed to calculate sensitivity
    data_json = to_json(data_obj)  # Serializing the data from objects to json
    initial_calculation = calculate_impacts(data_json)  # json data is posted to LCAbyg web API in calculate_impacts
    initial_building_impact_sum = find_building_sum(initial_calculation)  # find_building_sum locates the impact

    # Conduct sensitivity analysis for all product amounts in the wall
    sens_coeffs, product_names = sensitivity_of_file(data_obj, initial_building_impact_sum, 0.9)

    # Visualize the results based on the sensitivity coefficients for each product
    sensitivity_levels = how_sensitive_plural(sens_coeffs)
    print(f'Bar plot shows the sensitivity coefficient for each product. Coefficients are shown on the x-axis. \n'
          f'For the colors of the bars, green indicates low sensitivity, yellow medium and red high and very high.')
    bar_plot(product_names, sens_coeffs, sensitivity_levels, 'Sensitivity')


if __name__ == '__main__':
    main()
