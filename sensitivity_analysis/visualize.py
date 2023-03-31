import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
from typing import List


def bar_plot(names: List[str], values: List[float], sensitivity_levels: List[str], title: str):
    """
    Plot to illustrate the sensitivity of the products in the wall. Is a horizontal bar plot.
    The sensitivity coefficients are plotted for each product and the bars are colored to show the
    level of sensitivity
    The higher the sensitivity coefficient, the more sensitive the impact is to perturbation in the product amount.

    :param names: Names of the products as list with str
    :param values: sensitivity coefficients in a list
    :param sensitivity_levels: level of sensitivity as str in a list
    :param title: The title of the plot
    :return: Will show the plot
    """
    # Adjusts the size of the plot, which are given in inches, therefore the translation from cm
    cm = 1 / 2.54  # cm to inches
    fig, ax = plt.subplots(figsize=(26.48 * cm, 15 * cm))

    # Gets the colors for the plot
    colors = colors_for_bar_plot_sensitivity_level(sensitivity_levels)

    # The actual plot and the content for the plot
    ax.barh(names, values, color=colors, align='center', height=0.5)
    plt.title(title)
    plt.xlabel('Sensitivity coefficients')
    plt.ylabel('Products')

    # This ensures that the y-axis labels (product names) are visible
    make_axes_area_auto_adjustable(ax)

    # The plot will be shown and can be copied as an image by right-clicking
    plt.show()


def colors_for_bar_plot_sensitivity_level(sensitivity_levels: List[str]):
    """
    The colors are chosen based on the level of sensitivity to make the plot more illustrative.
    sensitivity_coefficient < 0.3 is low sensitivity
    0.3 <= sensitivity_coefficient < 0.5 is medium sensitivity
    0.5 <= sensitivity_coefficient < 1.0 is high sensitivity
    1.0 <= sensitivity_coefficient is very high sensitivity

    :param sensitivity_levels: level of sensitivity as str in a list
    :return: list with matplotlib color names
    """
    color_list = []

    for level in sensitivity_levels:
        if level == 'low':
            color_list.append('limegreen')
        elif level == 'medium':
            color_list.append('yellow')
        elif level == 'high':
            color_list.append('red')
        else:
            color_list.append('red')

    return color_list
