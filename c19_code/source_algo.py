import pandas as pd
from pdb import set_trace

def compute_row_algo(df):
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

    output=""

    if df["facteurs_gravite_majeur__au_moins_1"]:#L10
        output = "FIN5"#L11

    elif df["fievre__oui"] and df["toux__oui"]:#L14
        if df["facteurs_pronostiques__0"]:#L15
            output = "FIN6"#L16
        elif df["facteurs_pronostiques__au_moins_1"]:#L18
            if df["facteurs_gravite_mineur__0"] or \
                df["facteurs_gravite_mineur__1"]:#L19
                output = "FIN6"#L20
            elif df["facteurs_gravite_mineur__2"]:#L22
                output = "FIN4"#L23
            else:
                output = "ERROR"#This branch should not be possible
        else:
            output = "ERROR"#This branch should not be possible

    elif df["fievre__oui"] or df["diarrhee__oui"] or \
        (df["toux__oui"] and df["douleurs__oui"]) or \
        (df["toux__oui"] and df["anosmie__oui"]):#L28
        if df["facteurs_pronostiques__0"]:#L29
            if df["facteurs_gravite_mineur__0"]:#L30
                if df["age__moins_de_50"]:#L31
                    output = "FIN2"#L32
                elif df["age__plus_de_50"]:#L34
                    output = "FIN3"#L35
                else:
                    output = "ERROR"#This branch should not be possible
            elif df["facteurs_gravite_mineur__1"] or df["facteurs_gravite_mineur__2"]:#L38
                output = "FIN3"#L39
            else:
                output = "ERROR"#This branch should not be possible
        elif df["facteurs_pronostiques__au_moins_1"]:#L42
            if df["facteurs_gravite_mineur__0"] or df["facteurs_gravite_mineur__1"]:#L43
                output = "FIN3"#L44
            elif df["facteurs_gravite_mineur__2"]:#L46
                output = "FIN4"#L47
            else:
                output = "ERROR"#This branch should not be possible
        else:
            output = "ERROR"#This branch should not be possible

    elif df["toux__oui"] or df["douleurs__oui"] or df["anosmie__oui"]:#L52
        if df["facteurs_pronostiques__0"]:#L53
            output = "FIN2"#L54
        elif df["facteurs_pronostiques__au_moins_1"]:#L56
            output = "FIN7"#L57
        else:
            output = "ERROR"#This branch should not be possible
    else:#L61
        output = "FIN8"#L62



    if output == "ERROR":
        print("---ERROR: Impossible branch in source_algo---")
        print(df)
        set_trace()

    return output
    


def compute_df_algo(df):

    output = df.apply(
        lambda x: compute_row_algo(x),
        axis=1
    )

    return output
