import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

#  Load the cleaned dataset
df = pd.read_csv("IBM_Capstone_SpaceX/dataset_part_2_wrangled.csv")

#  Initialize the Dash app
app = dash.Dash(__name__)
app.title = "SpaceX Launch Dashboard"

# Define app layout
app.layout = html.Div(children=[
    html.H1(
        "🚀 SpaceX Launch Records Dashboard",
        style={'textAlign': 'center', 'color': '#003366', 'fontSize': 35}),
    
    html.Div([
        html.Label("Select Launch Site:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                    [{'label': site, 'value': site} for site in df['LaunchSite'].unique()],
            value='ALL',
            placeholder="Select a Launch Site",
            searchable=True),]
             , style={'width': '80%', 'margin': 'auto'}),

    html.Br(),

# Pie chart for success counts
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.Div([
        html.Label("Select Payload Range (kg):", style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=df['PayloadMass'].max(), step=1000,
            marks={i: f'{i}' for i in range(0, int(df['PayloadMass'].max())+1, 2000)},
            value=[df['PayloadMass'].min(), df['PayloadMass'].max()]),
    ], style={'width': '80%', 'margin': 'auto'}),

    html.Br(),

# Scatter chart for correlation
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# Callback for pie chart update
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))

def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(df, names='LaunchSite', values='LandingOutcome', 
                     title='Total Successful Launches by Site',
                     color_discrete_sequence=px.colors.sequential.RdBu)
    else:
        filtered_df = df[df['LaunchSite'] == selected_site]
        fig = px.pie(filtered_df, names='Outcome',
                     title=f'Success vs Failure for {selected_site}',
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
    return fig

#  Callback for scatter chart update
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')])

def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = df[(df['PayloadMass'] >= low) & (df['PayloadMass'] <= high)]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]

    fig = px.scatter(
        filtered_df, x='PayloadMass', y='LandingOutcome',
        color='BoosterVersion', hover_data=['LaunchSite', 'Outcome'],
        title='Correlation between Payload and Success Rate')
    return fig

# Roar the app auto-launch in browser for maximum coolness
#  Run the app — auto-launch in browser for maximum coolness
if __name__ == '__main__':
    import webbrowser
    import threading

    # open the app automatically in your default browser
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")

    # start the browser thread first
    threading.Timer(1.5, open_browser).start()

    # then run the Dash app
    app.run(debug=False, port=8050) #Debug = False for it not to auto re run with every edit i make on the poor program 
    # if u wanna re run or smth go to therminal and press Ctrl c it will brethe again and will stop being too busy hosting 