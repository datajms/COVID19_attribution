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


## 3. Run experiments
from c19_code.sample import get_saltelli_sample
from SALib.analyze import sobol

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

        ### 3.1. Generate random variable permutation
        # We randomize the order of columns to create randomization for Sobol
        # method, which is deterministic otherwise.
        perm = np.random.permutation(problem['num_vars'])
        problem_randomized = problem.copy()
        problem_randomized['names'] = [problem['names'][i] for i in perm]
        problem_randomized['bounds'] = [problem['bounds'][i] for i in perm]


        ### 3.2. Compute Saltelli samples
        df_sample = get_saltelli_sample(problem_randomized, 10000, calc_second_order=False)

        ### 3.3. Apply decision function (model)
        Y = f_algo(df_sample)

        ### 3.4. Perform Sobol Indices computation
        Si = sobol.analyze(problem_randomized, Y, print_to_console=False, calc_second_order=False)
        df_Sobol = pd.DataFrame(Si, index= problem_randomized['names'])

        ### 3.5. Post-process and log it
        sobol_total_list = []
        for variable in sorted(VAR_DICT_NO_MSF.keys()):
            sobol_total_list.append("{:.5f}".format(df_Sobol['ST'][variable]))

        sobol_str = ';'.join(sobol_total_list)

        logger.info('SOBOL_TOTAL;{};{}'.format(scenario, sobol_str))
