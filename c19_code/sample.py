import numpy as np
import pandas as pd
from SALib.sample import saltelli
import openturns as ot


def get_saltelli_sample(
    problem: dict, n_saltelli: int, calc_second_order: bool = False
) -> pd.DataFrame:
    """Encapsulates Saltelli sampling function from SALib

    Parameters
    ----------
    problem: dict
        problem definition in SALib format (see problem.py)
    n_saltelli: int
        'N' parameter of SALib.sample.saltelli: The number of samples to
        generate
    calc_second_order: bool
        'calc_second_order' parameter of SALib.sample.saltelli:
        Option to compute second order Sobol indices

    Returns
    -------
    df_sample: pd.DataFrame
        dataframe of Saltelli samples
    """
    param_values = saltelli.sample(
        problem, n_saltelli, calc_second_order=calc_second_order
    )

    # Replace column names
    df_sample = pd.DataFrame(param_values, columns=problem["names"])

    return df_sample


def problem_to_ot_distribution(problem):
    """
    Generate openturns distributions from problem.
    It is used by shapley-effects library.

    Parameters
    ----------
    problem: dict
        problem definition in SALib format (see problem.py)

    Returns
    -------
    input_distribution: a multi-variate openturns distributions
    """
    margins = []
    for i_var, variable in enumerate(problem["names"]):
        margins.append(
            ot.Uniform(problem["bounds"][i_var][0], problem["bounds"][i_var][1])
        )

    input_distribution = ot.ComposedDistribution(margins)

    return input_distribution
