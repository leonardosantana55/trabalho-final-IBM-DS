# Import required libraries
from fsspec import Callback
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Label('Dropdown'),
                                dcc.Dropdown(id='drop', 
                                            options=[{'label': 'All sites','value': 'ALL'},
                                                    {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E','value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40','value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True
                                ),
                                html.Br(),
                                

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Label('Slider'),
                                dcc.RangeSlider(min_payload, max_payload, 200, value=[min_payload,max_payload], id='slider'),
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('drop','value')
    )
def  update_figure(launch_site):
    df_filtered = spacex_df[spacex_df['Launch Site'].str.contains(launch_site)]
    df_count = df_filtered['class'].value_counts().to_frame().reset_index()
    df_count['index'].replace(0,'failed',inplace=True)
    df_count['index'].replace(1,'success',inplace=True)
    
    if launch_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Sucessfull landings by site')
        return fig
    else:
        title = 'sucess rate of ' + launch_site
        fig2 = px.pie(df_count, values='class', names='index', title=title)
        return fig2

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('drop','value'),
    Input('slider','value')
)
def update_scatter(launch_site, slider_value):
    df_ls = spacex_df[spacex_df['Launch Site'].str.contains(launch_site)]
    df_filtered_all = spacex_df[(spacex_df['Payload Mass (kg)'] > slider_value[0]) & (spacex_df['Payload Mass (kg)'] < slider_value[1])]
    df_filtered_ls = df_ls[(df_ls['Payload Mass (kg)'] > slider_value[0]) & (df_ls['Payload Mass (kg)'] < slider_value[1])]
    
    if launch_site == 'ALL':
        figall = px.scatter(df_filtered_all, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figall
    else:
        figls = px.scatter(df_filtered_ls, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figls
    pass

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)