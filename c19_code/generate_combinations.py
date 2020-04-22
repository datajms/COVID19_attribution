import numpy as np
import pandas as pd

VAR_DICT = {
    "age": ["49_or_less", "50_or_more"],
    "fever": ["no", "yes"],
    "cough": ["no", "yes"],
    "sore_throat_aches": ["no", "yes"],
    "anosmia": ["no", "yes"],
    "diarrhea": ["no", "yes"],
    "risk_factor": ["0", "1_or_more"],
    "minor_severity_factor": ["0", "1", "2"],
    "major_severity_factor": ["0", "1_or_more"],
}


def get_all_combinations(var_dict: dict, dummify: bool = True) -> pd.DataFrame:
    """
    Generate all combinations of variables from var_dict, a dict of
    variable names (keys) and their category names (values).
    Output is a pandas DataFrame with each row being a unique combination.
    Dummification is an option:
    - if yes: render a 0/1 dataframe with column names being in format
    variable__category
    - if no: render a str dataframe with the name of categories. Column names
    are the variable names.

    Parameters
    ----------
    var_dict: dict
        dict of variable names (keys) and their category names (values)
    dummify: bool optional
        dummification (one-hot encoding) option of dataframe

    Returns
    -------
    output: pd.DataFrame
        All combinations in the correct format (dummified or not).
    """
    n_dict = len(var_dict)

    # To save space, strings are not used inside the array or DataFrame at this step.
    # Integers are used instead
    comb_array = np.array(
        np.meshgrid(
            *([i for i, _ in enumerate(v)] for _, v in sorted(var_dict.items()))
        )
    ).reshape(-1, n_dict)

    if dummify:
        # Convert to dataframe and perform dummification
        df_output = pd.get_dummies(
            pd.DataFrame(comb_array),
            columns=[i for i in range(n_dict)],
            drop_first=False,
            prefix_sep="__",
        )

        # Replace the column names (in i_var__i_cat format) with string names
        # in var__cat format
        renaming_dict = {}
        i_variable = 0
        for variable, category_list in sorted(var_dict.items()):
            for i_category, category in enumerate(category_list):
                name_before = str(i_variable) + "__" + str(i_category)
                name_after = variable + "__" + category
                renaming_dict[name_before] = name_after
            i_variable += 1

        df_output.rename(columns=renaming_dict, inplace=True)

    else:  # No dummification
        # Convert to dataframe and replace the integer column names by strings
        df_output = pd.DataFrame(comb_array, columns=sorted(var_dict.keys()))

        # Replace the integer category names by strings
        for variable, category_list in sorted(var_dict.items()):
            renaming_dict = {}
            for i_category, category in enumerate(category_list):
                renaming_dict[str(i_category)] = category
            df_output[variable] = df_output[variable].astype(str)
            df_output[variable].replace(renaming_dict, inplace=True)

    return df_output
