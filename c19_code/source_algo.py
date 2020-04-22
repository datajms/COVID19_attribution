import pandas as pd
from pdb import set_trace


def compute_row_algo(df: pd.Series) -> str:
    """This algorithm is based on recommandations of AP-HP and the Pasteur
    Institute, on Friday, the 30th of March 2020.
    Check https://delegation-numerique-en-sante.github.io/covid19-algorithme-orientation/algorithme-orientation-covid19.html
     and the associated github for more information.

    The line numbers indicated come from https://github.com/Delegation-numerique-en-sante/covid19-algorithme-orientation/blob/master/diagramme.org

    Parameters
    ----------
    df: pd.Series
        A row of a dataframe. Columns should strictly match names in the conditions below
    """

    output = ""

    if df["major_severity_factor__1_or_more"]:  # L10
        output = "END5"  # L11

    elif df["fever__yes"] and df["couch__yes"]:  # L14
        if df["risk_factor__0"]:  # L15
            output = "END6"  # L16
        elif df["risk_factor__1_or_more"]:  # L18
            if df["minor_severity_factor__0"] or df["minor_severity_factor__1"]:  # L19
                output = "END6"  # L20
            elif df["minor_severity_factor__2"]:  # L22
                output = "END4"  # L23
            else:
                output = "ERROR"  # This branch should not be possible
        else:
            output = "ERROR"  # This branch should not be possible

    elif (
        df["fever__yes"]
        or df["diarrhea__yes"]
        or (df["couch__yes"] and df["sore_throat_aches__yes"])
        or (df["couch__yes"] and df["anosmia__yes"])
    ):  # L28
        if df["risk_factor__0"]:  # L29
            if df["minor_severity_factor__0"]:  # L30
                if df["age__49_or_less"]:  # L31
                    output = "END2"  # L32
                elif df["age__50_or_more"]:  # L34
                    output = "END3"  # L35
                else:
                    output = "ERROR"  # This branch should not be possible
            elif (
                df["minor_severity_factor__1"] or df["minor_severity_factor__2"]
            ):  # L38
                output = "END3"  # L39
            else:
                output = "ERROR"  # This branch should not be possible
        elif df["risk_factor__1_or_more"]:  # L42
            if df["minor_severity_factor__0"] or df["minor_severity_factor__1"]:  # L43
                output = "END3"  # L44
            elif df["minor_severity_factor__2"]:  # L46
                output = "END4"  # L47
            else:
                output = "ERROR"  # This branch should not be possible
        else:
            output = "ERROR"  # This branch should not be possible

    elif df["couch__yes"] or df["sore_throat_aches__yes"] or df["anosmia__yes"]:  # L52
        if df["risk_factor__0"]:  # L53
            output = "END2"  # L54
        elif df["risk_factor__1_or_more"]:  # L56
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


def compute_df_algo(df: pd.DataFrame) -> pd.Series:
    output = df.apply(lambda x: compute_row_algo(x), axis=1)

    return output
