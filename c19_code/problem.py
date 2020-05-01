## Generate data to set-up the problem of Covid-19 orientation
"""This algorithm is based on recommandations of AP-HP and the Pasteur
Institute, on Friday, the 30th of March 2020.
Check https://delegation-numerique-en-sante.github.io/covid19-algorithme-orientation/algorithme-orientation-covid19.html
 and the associated github for more information."""

VAR_DICT = {
    "age": ["49_or_less", "50_or_more"],
    "anosmia": ["no", "yes"],
    "cough": ["no", "yes"],
    "diarrhea": ["no", "yes"],
    "fever": ["no", "yes"],
    "major_severity_factor": ["0", "1_or_more"],
    "minor_severity_factor": ["0", "1", "2"],
    "risk_factor": ["0", "1_or_more"],
    "sore_throat_aches": ["no", "yes"],
}

# Remove major_severity_factor from analysis :
VAR_DICT_NO_MSF = VAR_DICT.copy()
VAR_DICT_NO_MSF.pop("major_severity_factor")


VAR_THRESH_A = {
    "age": 0.5,
    "fever": 0.2,
    "cough": 0.2,
    "sore_throat_aches": 0.2,
    "anosmia": 0.2,
    "diarrhea": 0.2,
    "risk_factor": 0.2,
    "minor_severity_factor": 0.2,
}

VAR_THRESH_B = {
    "age": 0.5,
    "fever": 0.5,
    "cough": 0.5,
    "sore_throat_aches": 0.5,
    "anosmia": 0.5,
    "diarrhea": 0.5,
    "risk_factor": 0.5,
    "minor_severity_factor": 0.5,
}


def problem_from_var_dict(var_dict: dict) -> dict:
    """
    Initialy used by the SALib framework, we keep the problem dict
    for all methods

    Parameters
    ----------
    var_dict: dict
        var_dict where keys are variable names and values are the names
        of the categories

    Returns
    -------
    problem: dict
        problem formulation of SALib: dict with useful keys: num_vars (number
        of variables), names (variables names) and bounds (bounds of uniform
        distribution of variables)
    """
    problem = {
        "num_vars": len(var_dict.keys()),
        "names": sorted(list(var_dict.keys())),
        "bounds": [[0.0, 1.0]] * len(var_dict.keys()),
    }

    return problem
