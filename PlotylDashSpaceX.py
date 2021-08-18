# Import required libraries
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
listLaunchSites = spacex_df['Launch Site'].unique()

df = px.data.tips()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='sitedropdown',
                                    options=[{'value': 'ALL', 'label': 'ALL'},
                                    {'value': listLaunchSites[0], 'label': listLaunchSites[0]},
                                    {'value': listLaunchSites[1], 'label': listLaunchSites[1]},
                                    {'value': listLaunchSites[2], 'label': listLaunchSites[2]},
                                    {'value': listLaunchSites[3], 'label': listLaunchSites[3]}
                                    ],
                                    value = 'ALL',
                                    placeholder = 'Select a Launch Site here',
                                    searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                 dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),
                                html.Div(id='output-container-range-slider'),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='sitedropdown', component_property='value'))

# Add computation to callback function and return graph
def generate_chart(sitedropdown):
    if sitedropdown == 'ALL':
        fig = px.pie(spacex_df, "Launch Site","class")
    else:
        dfspaceX_A = spacex_df[spacex_df["Launch Site"]==sitedropdown]
        fig = px.pie(dfspaceX_A, "class")
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='sitedropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

# Add computation to callback function and return graph
def update_output(sitedropdown,y):
    if sitedropdown == 'ALL':
        dfspaceX_C = spacex_df[spacex_df["Payload Mass (kg)"].between(y[0], y[1], inclusive='both')]
    else:
        dfspaceX_A = spacex_df[spacex_df["Launch Site"]==sitedropdown]
        dfspaceX_C = dfspaceX_A[dfspaceX_A["Payload Mass (kg)"].between(y[0], y[1], inclusive='both')]
        
    fig2 = px.scatter(dfspaceX_C,"Payload Mass (kg)","class", color="Booster Version Category")
    return fig2

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('payload-slider', 'value')])
def slidervalue(value):
    return 'You have selected "{}"'.format(value)
# Run the app
if __name__ == '__main__':
    app.run_server()
