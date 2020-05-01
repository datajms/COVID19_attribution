import logging
import os

LOGGER_FILE = '../data_n_figures/all_experiments_results.csv'

from c19_code.problem import VAR_DICT_NO_MSF

if __name__=='__main__':
    if os.path.isfile(LOGGER_FILE):
        os.remove(LOGGER_FILE)

    ## Init logging file
    init_logger = logging.getLogger()
    init_logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(filename=LOGGER_FILE)
    init_logger.addHandler(ch)

    from c19_code.problem import VAR_DICT_NO_MSF
    factor_list = ';'.join(sorted(VAR_DICT_NO_MSF.keys()))
    init_logger.info("timestamp;importance_type;scenario;{}".format(factor_list))


## Set-up logger for scripts
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler(filename=LOGGER_FILE)
logger.addHandler(ch)
formatter = logging.Formatter('%(asctime)s;%(message)s')
ch.setFormatter(formatter)
