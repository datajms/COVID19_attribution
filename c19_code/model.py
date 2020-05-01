import pandas as pd
import numpy as np
from pdb import set_trace


def compute_row_algo(df: pd.Series) -> str:
    """This algorithm is based on recommandations of AP-HP and the Pasteur
    Institute, on Friday, the 30th of March 2020.
    Check https://delegation-numerique-en-sante.github.io/covid19-algorithme-orientation/algorithme-orientation-covid19.html
     and the associated github for more information.

    The line numbers indicated come from
    https://github.com/Delegation-numerique-en-sante/covid19-algorithme-orientation/blob/master/diagramme.org

    Parameters
    ----------
    df: pd.Series
        A row of a dataframe. Columns should strictly match names in
        the conditions below
    """

    output = ""

    # If major_severity_factor is not present, we do as if it were "0"
    # Functional design trick to quickly handle case where we focus on
    # Non-emergency paths.
    if "major_severity_factor" not in df.index:
        major_severity_factor = "0"
    else:
        major_severity_factor = df["major_severity_factor"]

    if major_severity_factor == "1_or_more":  # L10
        output = "END5"  # L11

    elif df["fever"] == "yes" and df["cough"] == "yes":  # L14
        if df["risk_factor"] == "0":  # L15
            output = "END6"  # L16
        elif df["risk_factor"] == "1_or_more":  # L18
            if (
                df["minor_severity_factor"] == "0" or df["minor_severity_factor"] == "1"
            ):  # L19
                output = "END6"  # L20
            elif df["minor_severity_factor"] == "2":  # L22
                output = "END4"  # L23
            else:
                output = "ERROR"  # This branch should not be possible
        else:
            output = "ERROR"  # This branch should not be possible

    elif (
        df["fever"] == "yes"
        or df["diarrhea"] == "yes"
        or (df["cough"] == "yes" and df["sore_throat_aches"] == "yes")
        or (df["cough"] == "yes" and df["anosmia"] == "yes")
    ):  # L28
        if df["risk_factor"] == "0":  # L29
            if df["minor_severity_factor"] == "0":  # L30
                if df["age"] == "49_or_less":  # L31
                    output = "END2"  # L32
                elif df["age"] == "50_or_more":  # L34
                    output = "END3"  # L35
                else:
                    output = "ERROR"  # This branch should not be possible
            elif (
                df["minor_severity_factor"] == "1" or df["minor_severity_factor"] == "2"
            ):  # L38
                output = "END3"  # L39
            else:
                output = "ERROR"  # This branch should not be possible
        elif df["risk_factor"] == "1_or_more":  # L42
            if (
                df["minor_severity_factor"] == "0" or df["minor_severity_factor"] == "1"
            ):  # L43
                output = "END3"  # L44
            elif df["minor_severity_factor"] == "2":  # L46
                output = "END4"  # L47
            else:
                output = "ERROR"  # This branch should not be possible
        else:
            output = "ERROR"  # This branch should not be possible

    elif (
        df["cough"] == "yes"
        or df["sore_throat_aches"] == "yes"
        or df["anosmia"] == "yes"
    ):  # L52
        if df["risk_factor"] == "0":  # L53
            output = "END2"  # L54
        elif df["risk_factor"] == "1_or_more":  # L56
            output = "END7"  # L57
        else:
            output = "ERROR"  # This branch should not be possible
    else:  # L61
        output = "END8"  # L62

    if output == "ERROR":
        print("---ERROR: Impossible branch in source_algo---")
        print(df)
        set_trace()

    return output


def compute_df_algo(
    df_float: pd.DataFrame, var_dict: dict, var_thresh: dict = {}
) -> pd.Series:
    """
    Run compute_row_algo from a pd.DataFrame (or np.array).
    Inputs in df_float should be floats, which are converted to str categories
    with var_dict and var_thresh.

    Parameters
    ----------
    df_float: pd.DataFrame or np.ndarray
        Input DataFrame, on which is applied compute_row_algo function, row
        by row. df_float contains float in 0-1,
        on which are applied the var_thresh thresholds
    var_dict: dict
        var_dict (dict where keys are variable names and values are the names
        of the categories) is used to convert the 0-1 floats into category str
        example: [0.02, 0.4, 0.9] would become ['no', 'no', 'yes'], for variable
        fever. It is used in combination with var_thresh.
        If df_float is a np.ndarray, we retrieve the column names with
        sorted(var_dict.keys()).
    var_thresh: dict, optional {}
        var_thresh is a dict where keys are variable name and values are
        a float between 0 and 1. It represents the threshold, to convert the
        input floats into str.
        If a variable is not in var_thresh, the default threshold is 0.5.

    Returns
    -------
    output: pd.Series
        Output pandas Series with algorithm results, row by row
    """
    if type(df_float) == pd.DataFrame:
        df_str = df_float.copy()
    elif type(df_float) == np.ndarray:
        df_str = pd.DataFrame(df_float.copy(), columns=sorted(var_dict.keys()))
    else:
        raise TypeError(
            """Input should be either a pd.DataFrame or a
        np.ndarray, not {}""".format(
                type(df_float)
            )
        )
    default_probability = 0.5

    for variable in df_str.columns:
        if variable not in var_thresh.keys():
            var_thresh[variable] = default_probability

    # Rounding float values so that we can replace it by the str categories
    for variable in df_str.columns:
        # Assume that there are exactly 2 categories by variable
        category_of_lower_risk = var_dict[variable][0]
        category_of_higher_risk = var_dict[variable][1]

        df_str[variable] = df_str[variable].apply(
            lambda x: category_of_lower_risk
            if x <= 1 - var_thresh[variable]
            else category_of_higher_risk
        )
        # 2 principles here:
        # - float near 0 should lead to the category of lowest risk.
        # - var_thresh should represent the probability of the
        # highest risk category

    output = df_str.apply(lambda x: compute_row_algo(x), axis=1)

    return output


def simplified_algo(official_outcome: pd.Series, as_str: bool = False) -> pd.Series:
    """
    Apply simplification mapping to the outcomes of official algorithm.
    Output are in integer format by default;
    or str format if as_str is set to True.

    Parameters
    ----------
    official_outcome: pd.Series
        official outcomes, as a pandas Series of str

    as_str: bool, optional
        if True, outputs are in str format; if False, as integer

    Returns
    -------
    simplified_outcome: pd.Series
        the simplified outcomes, as a pandas Series of str or integer

    """

    # The official outcome END1 means that the under 15 years of age are
    # not covered by the algorithm. This case is therefore not dealt by
    # the simplified mapping
    simplified_mapping = {
        "END2": 0,  # No action
        "END3": 1,  # Teleconsultation
        "END4": 1,  # Teleconsultation, if pb call emergency services
        "END5": 2,  # Call emergency services
        "END6": 1,  # Teleconsultation
        "END7": 1,  # Teleconsultation, if pb call emergency services
        "END8": 0,  # No action
    }

    str_mapping = {0: "no_action", 1: "teleconsultation", 2: "emergency"}

    simplified_outcome = official_outcome.map(simplified_mapping)
    if as_str:
        simplified_outcome = simplified_outcome.map(str_mapping)

    return simplified_outcome


def simplified_teleconsultation_vs_noaction(
    input: pd.DataFrame, var_dict: dict, var_thresh: dict = {}
) -> np.array:
    """Final encapsulation of simplified_algo and compute_df_algo,
    so that the output is an array

    Parameters
    ----------
    input: pd.DataFrame or np.ndarray
        dataframe passed into compute_df_algo (see desc. there)
    var_dict: dict
        dict passed into compute_df_algo (see desc. there)
    var_thresh: dict
        dict passed into compute_df_algo (see desc. there)

    Returns
    -------
    output: np.ndarray
        array of the outcome of simplified_algo. 1.0 means teleconsultation
        while 0.0 means no action required.
    """
    output = np.array(
        simplified_algo(
            compute_df_algo(input, var_dict, var_thresh=var_thresh), as_str=False
        )
    )
    return output
