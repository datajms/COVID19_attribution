import pandas as pd
import numpy as np


## 1. Load results csv
from experiments.my_logger import LOGGER_FILE
df_raw = pd.read_csv('../data_n_figures/'+LOGGER_FILE, sep=';', header=0)

## 2. Aggregate by importance_type and scenario

agg_function_list = ['mean', 'min', 'max']
agg_importances = {}
for f_agg in agg_function_list:
    agg_importances[f_agg] = df_raw\
        .drop(['timestamp'], axis=1)\
        .groupby(['importance_type', 'scenario'])\
        .agg(f_agg)

raw_factor_columns = agg_importances['mean'].columns.tolist()
n_factor = len(raw_factor_columns)

## 3. Normalize importances (so that they add up to 100% in average)
importance_list = ['SOBOL_TOTAL', 'SHAPLEY_EFFECT', 'SHAP_IMPORTANCE']
final_importances = {}
raw_imp_sum = {}
for imp in importance_list:
    for scenario in ['A', 'B']:
        raw_imp_sum[(imp, scenario)] = agg_importances['mean'].loc[(imp, scenario)].sum()
        print('Raw sum of {} in scenario {}: {:.5f}'.format(imp, scenario, raw_imp_sum[(imp, scenario)]))

        for f_agg in agg_function_list:
             final_importances[(scenario, imp, f_agg)] = agg_importances[f_agg].loc[(imp, scenario)] *\
                100.0/raw_imp_sum[(imp, scenario)] # *100 to have it expressed as percentages

## 4. Create AVERAGE_IMPORTANCE, a measure of importance which is the average of the 3 normalized  importances
for scenario in ['A', 'B']:
    final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'mean')] =\
        1.0/3 * final_importances[(scenario, importance_list[0], 'mean')]+\
        1.0/3 * final_importances[(scenario, importance_list[1], 'mean')]+\
        1.0/3 * final_importances[(scenario, importance_list[2], 'mean')]


## 5. For 'min' and 'max', the AVERAGE IMPORTANCE is computed by taking min and max of 50 averages.

for scenario in ['A', 'B']:
    final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'min')] = 100.0 * np.ones(n_factor) # Initialization
    final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'max')] = np.zeros(n_factor) # Initialization

    for i_exp in range(50):
        current_average = np.zeros(n_factor)
        for imp in importance_list:
            sample_imp = np.array(df_raw.query("importance_type==@imp and scenario==@scenario")\
                .drop(['timestamp', 'importance_type', 'scenario'], axis=1)\
                .sample(1).T).reshape(-1)
            sample_imp *= 100.0/raw_imp_sum[(imp, scenario)]
            current_average += 1.0/3 * sample_imp

        final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'min')] =\
            np.minimum(final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'min')],
                        current_average)
        final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'max')] =\
            np.maximum(final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'max')],
                        current_average)

    final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'min')] =\
        pd.Series(final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'min')], index=raw_factor_columns)
    final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'max')] =\
        pd.Series(final_importances[(scenario, 'AVERAGE_IMPORTANCE', 'max')], index=raw_factor_columns)

## 6. Reorder factors by increasing value of AVERAGE_IMPORTANCE of sc. A

factor_order = final_importances[('A', 'AVERAGE_IMPORTANCE', 'mean')].sort_values().index.tolist()
factor_order

for scenario in ['A', 'B']:
    for imp in importance_list+['AVERAGE_IMPORTANCE']:
        for f_agg in agg_function_list:
            final_importances[(scenario, imp, f_agg)] = final_importances[(scenario, imp, f_agg)].reindex(factor_order)



from plotly.subplots import make_subplots
import plotly.graph_objects as go

from c19_code.plot import clean_variable_names, legend_imp_name, color_imp_name
from c19_code.plot import x_axis_setting_tick, x_axis_setting, y_axis_setting

factor_label = final_importances[('A', 'AVERAGE_IMPORTANCE', 'mean')].index.map(
    clean_variable_names)


fig = make_subplots(rows=2, cols=2, shared_yaxes=True, shared_xaxes=True,
                    vertical_spacing=0.08,
                    horizontal_spacing=0.05,
                    subplot_titles=("scenario A - all importances", "scenario B - all importances",
                                   "scenario A - average importance", "scenario B - average importance"))


for i_scenario, scenario in enumerate(['A', 'B']):
    for imp in ['SHAP_IMPORTANCE', 'SHAPLEY_EFFECT' , 'SOBOL_TOTAL']:
        fig.add_trace(go.Bar(
                        x=final_importances[(scenario, imp, 'mean')],
                        y=factor_label,
                        name=legend_imp_name[imp],
                        error_x=dict(
                            type='data',
                            symmetric=False,
                            array=final_importances[(scenario, imp, 'max')] - final_importances[(scenario, imp, 'mean')],
                            arrayminus=final_importances[(scenario, imp, 'mean')] - final_importances[(scenario, imp, 'min')]
                        ),
                        marker_color=color_imp_name[imp],
                        orientation='h',
                        showlegend= (scenario=='B')
                        ),
                     1, #row of subplot
                     i_scenario+1) #col of subplot

    imp = 'AVERAGE_IMPORTANCE'
    fig.add_trace(go.Bar(
                        x=final_importances[(scenario, imp, 'mean')],
                        y=factor_label,
                        name=legend_imp_name[imp],
                        error_x=dict(
                            type='data',
                            symmetric=False,
                            array=final_importances[(scenario, imp, 'max')] - final_importances[(scenario, imp, 'mean')],
                            arrayminus=final_importances[(scenario, imp, 'mean')] - final_importances[(scenario, imp, 'min')]
                        ),
                        marker_color=color_imp_name[imp],
                        orientation='h',
                        showlegend= (scenario=='B')
                        ),
                     2, #row of subplot
                     i_scenario+1) #col of subplot

fig.update_layout(
    xaxis4=x_axis_setting_tick,
    xaxis3=x_axis_setting_tick,
    xaxis2=x_axis_setting,
    xaxis=x_axis_setting,
    yaxis=y_axis_setting,
    yaxis2=y_axis_setting,
    yaxis3=y_axis_setting,
    yaxis4=y_axis_setting,
    legend=dict(
        x=0.77,
        y=0.64,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent factor.
    bargroupgap=0.1, # gap between bars of the same factor.
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig['layout'].update(height=600, width=1000)


#fig.show()

fig.write_html("../data_n_figures/all_importances_scenarios.html")


import plotly.express as px

factor_label = final_importances[('A', 'AVERAGE_IMPORTANCE', 'mean')].index.map(
    clean_variable_names)

fig = px.pie(None,
             values=final_importances[('A', 'AVERAGE_IMPORTANCE', 'mean')].apply(lambda x: round(x)),
             names=factor_label,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=19)
#fig.show()

fig.write_html("../data_n_figures/pie_chart.html")
