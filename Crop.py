import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

# Step 1: Load the dataset
df = pd.read_csv('Crop Production data.csv')

# Step 2: Data Transformation and Analysis
# Group by year to analyze yearly crop production
yearly_production = df.groupby('Crop_Year')[['Area', 'Production']].sum().reset_index()

# Compute yield (Production per unit area)
yearly_production['Yield'] = yearly_production['Production'] / yearly_production['Area']

# Seasonal Analysis
seasonal_production = df.groupby('Season')[['Area', 'Production']].sum().reset_index()
seasonal_production['Yield'] = seasonal_production['Production'] / seasonal_production['Area']

# State-wise Analysis
state_production = df.groupby('State_Name')[['Area', 'Production']].sum().reset_index()
state_production['Yield'] = state_production['Production'] / state_production['Area']

# Crop Type Analysis
crop_production = df.groupby('Crop')[['Area', 'Production']].sum().reset_index()
crop_production['Yield'] = crop_production['Production'] / crop_production['Area']

# Step 3: Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 4: Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Crop Production Analysis Dashboard"),
    
    # Yearly crop production and yield trends
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='yearly-production',
                      figure=px.line(yearly_production, x='Crop_Year', y='Production', 
                                     title='Yearly Crop Production Trends')),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='yield-trend',
                      figure=px.line(yearly_production, x='Crop_Year', y='Yield', 
                                     title='Yearly Yield Trends')),
            width=6
        )
    ]),
    
     # Seasonal crop production and yield analysis
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='seasonal-production',
                      figure=px.bar(seasonal_production, x='Season', y='Production', 
                                    title='Seasonal Crop Production Analysis', color_discrete_sequence=['#00CC96'])),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='seasonal-yield',
                      figure=px.bar(seasonal_production, x='Season', y='Yield', 
                                    title='Seasonal Crop Yield Analysis', color_discrete_sequence=['#AB63FA'])),
            width=6
        )
    ]),

    # State-wise crop production and yield analysis
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='state-production',
                      figure=px.bar(state_production, x='State_Name', y='Production', 
                                    title='State-wise Crop Production Analysis', color_discrete_sequence=['#FFA15A'])),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='state-yield',
                      figure=px.bar(state_production, x='State_Name', y='Yield', 
                                    title='State-wise Crop Yield Analysis', color_discrete_sequence=['#19D3F3'])),
            width=6
        )
    ]),

    # Crop type production and yield analysis
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='crop-type-production',
                      figure=px.bar(crop_production, x='Crop', y='Production', 
                                    title='Crop Type Production Analysis', color_discrete_sequence=['#FF6692'])),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='crop-type-yield',
                      figure=px.bar(crop_production, x='Crop', y='Yield', 
                                    title='Crop Type Yield Analysis', color_discrete_sequence=['#B6E880'])),
            width=6
        )
    ]),
])

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

