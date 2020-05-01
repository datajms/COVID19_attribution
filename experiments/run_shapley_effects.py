import numpy as np
import pandas as pd
import logging


## 0. Config logger
from my_logger import logger

## 1. Load and set-up problem
from c19_code.problem import VAR_DICT_NO_MSF, problem_from_var_dict
from c19_code.problem import VAR_THRESH_A, VAR_THRESH_B

# Set-up problem
problem = problem_from_var_dict(VAR_DICT_NO_MSF)
N_EXPERIMENTS = 50

## 2. Load decision function (model)
from c19_code.model import simplified_teleconsultation_vs_noaction

## 3. Set-up parameters and run Shapley Effects
from c19_code.sample import problem_to_ot_distribution
from shapley.model import ProbabilisticModel
import openturns as ot
from shapley import ShapleyIndices

n_perms = 1000 # See Shapley Effect docs for meaning of parameters
n_var = 1000
n_outer = 50
n_inner = 7
n_boot = 500

for i_exp in range(N_EXPERIMENTS):
    for scenario in ['A', 'B']:
        if scenario=='A':
            # Define Covid-19 scenario A
            f_algo = lambda x: simplified_teleconsultation_vs_noaction(
                x,
                VAR_DICT_NO_MSF,
                var_thresh=VAR_THRESH_A)
        else:
            # Define Covid-19 scenario B
            f_algo = lambda x: simplified_teleconsultation_vs_noaction(
                x,
                VAR_DICT_NO_MSF,
                var_thresh=VAR_THRESH_B)


        ### 3.1. Build statistical model from problem
        input_distribution = problem_to_ot_distribution(problem)
        model = ProbabilisticModel(model_func=f_algo, input_distribution=input_distribution)

        ### 3.2. Generate random samples from statistical model
        shapley = ShapleyIndices(model.input_distribution)
        shapley.build_sample(model=model, n_perms=n_perms, n_var=n_var, n_outer=n_outer, n_inner=n_inner)

        ### 3.3. Perform Shapley Effects computation
        shapley_results = shapley.compute_indices(n_boot=n_boot)
        df_Shapley = pd.DataFrame({
            'S1': shapley_results.first_indices,
            'ST': shapley_results.total_indices,
            'She': shapley_results.shapley_indices.mean(axis=1)
        }, index= problem['names'])

        ### 3.5. Post-process and log it
        she_total_list = []
        for variable in sorted(VAR_DICT_NO_MSF.keys()):
            she_total_list.append("{:.5f}".format(df_Shapley['She'][variable]))

        she_str = ';'.join(she_total_list)

        logger.info('SHAPLEY_EFFECT;{};{}'.format(scenario, she_str))
