import numpy as np
import pandas as pd
import logging


## 0. Config logger
from my_logger import logger
logger.setLevel(logging.ERROR) # Silent logger, because SHAP is chatty.


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
import shap

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


        ### 3.1. Compute random samples for which shap values will be computed
        df_distribution = get_saltelli_sample(problem, 10000, calc_second_order=False)
        df_sample = df_distribution.sample(300) # We used saltelli_sample as
        # a random generator, but the final number of sample is given in this line

        ### 3.2. Init KernelShap
        reference = shap.sample(df_distribution, 50) # These samples are used to
        # compute to expectations of variables that are "shut-down" by shap.
        explainer = shap.KernelExplainer(f_algo, reference)


        ### 3.3. Perform shap values computation
        shap_values = explainer.shap_values(df_sample)

        ### 3.4. Aggregate over samples defined in 3.1. and log it
        df_shap = pd.Series(np.abs(shap_values).mean(axis=0), index= problem['names'])

        shap_total_list = []
        for variable in sorted(VAR_DICT_NO_MSF.keys()):
            shap_total_list.append("{:.5f}".format(df_shap[variable]))

        shap_str = ';'.join(shap_total_list)

        logger.setLevel(logging.DEBUG)
        logger.info('SHAP_IMPORTANCE;{};{}'.format(scenario, shap_str))
        logger.setLevel(logging.ERROR)
