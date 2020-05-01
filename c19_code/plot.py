## Some utils for plots

clean_variable_names = {
    "age": "Age",
    "anosmia": "Anosmia",
    "cough": "Cough",
    "diarrhea": "Diarrhea",
    "fever": "Fever",
    "minor_severity_factor": "Number of minor severity factors",
    "risk_factor": "Number of risk factors",
    "sore_throat_aches": "Sore throat/aches",
}

legend_imp_name = {
    "SOBOL_TOTAL": "Sobol Total-order",
    "SHAPLEY_EFFECT": "Shapley Effects",
    "SHAP_IMPORTANCE": "Shap Importance",
    "AVERAGE_IMPORTANCE": "Average Importance",
}

color_imp_name = {
    "SOBOL_TOTAL": "rgb(192,233,231)",
    "SHAPLEY_EFFECT": "rgb(252,236,147)",
    "SHAP_IMPORTANCE": "rgb(227,142,139)",
    "AVERAGE_IMPORTANCE": "rgb(56,108,176)",
}

x_axis_setting_tick = dict(
    title="Normalized importances (%)",
    titlefont_size=12,
    tickfont_size=10,
    range=[0, 30],
    tick0=0,
    dtick=5,
    showgrid=True,
    gridwidth=1,
    gridcolor="rgb(230,230,230)",
    showline=True,
    linecolor="black",
    mirror=True,
)

x_axis_setting = dict(
    tickfont_size=10,
    range=[0, 30],
    tick0=0,
    dtick=5,
    showgrid=True,
    gridwidth=1,
    gridcolor="rgb(230,230,230)",
    showline=True,
    linecolor="black",
    mirror=True,
)

y_axis_setting = dict(tickfont_size=10, showline=True, linecolor="black", mirror=True)
