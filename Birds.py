import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

# Step 1: Extract - Load the dataset
df = pd.read_csv('Bird Strikes data.csv', encoding='latin1')

# Remove null values
df.dropna(inplace=True)

# Convert 'Cost' column to numeric data type with errors='coerce'
df['Cost: Total $'] = pd.to_numeric(df['Cost: Total $'], errors='coerce')

df['FlightDate'] = pd.to_datetime(df['FlightDate'])

# Yearly analysis & bird strikes in the US
df['Year'] = df['FlightDate'].dt.year

# Group by year and sum the number of bird strikes
yearly_strikes = df.groupby('Year')['Wildlife: Number Struck Actual'].sum().reset_index()

# Create a line chart
yearly_line_chart = px.line(yearly_strikes, x='Year', y='Wildlife: Number Struck Actual', 
                            title='Yearly Analysis of Bird Strikes',
                            labels={'Wildlife: Number Struck Actual': 'Total Number of Bird Strikes'},
                            color_discrete_sequence=['#636EFA'])

# Top 10 US Airlines in terms of encountering bird strikes
top_airlines = px.bar(df.nlargest(11, 'Wildlife: Number Struck Actual'), x='Aircraft: Airline/Operator', y='Wildlife: Number Struck Actual', title='Top 10 US Airlines by Bird Strike Incidents',
                      color_discrete_sequence=['#EF553B'])

# Airports with most incidents of bird strikes - Top 50
top_airports = px.bar(df.nlargest(50, 'Wildlife: Number Struck Actual'), x='Airport', y='Wildlife: Number Struck Actual',
                      title='Top 50 Airports by Bird Strike Incidents',
                      color_discrete_sequence=['#00CC96'])

# Yearly cost incurred due to bird strikes
yearly_cost = px.bar(df.groupby('Year')['Cost: Total $'].sum().reset_index(), x='Year', y='Cost: Total $',
                     title='Yearly Cost Incurred due to Bird Strikes',
                     color_discrete_sequence=['#AB63FA'])

df['Feet above ground'] = df['Feet above ground'].str.replace(',', '').astype('int64')

# Altitude of airplanes at the time of strike
altitude_at_strike = px.histogram(df, x='Feet above ground', title='Distribution of Altitude at the Time of Bird Strike',
                                  color_discrete_sequence=['#FFA15A'],
                                  nbins=10)  # Adjust the number of bins as needed

# Phase of flight at the time of the strike
flight_phase_at_strike = px.bar(df['When: Phase of flight'].value_counts().reset_index(), x='index', y='When: Phase of flight',
                                title='Distribution of Bird Strikes by Phase of Flight',
                                color_discrete_sequence=['#19D3F3'])

# Average altitude of the airplanes in different phases at the time of strike
avg_altitude_by_phase = px.bar(df.groupby('When: Phase of flight')['Feet above ground'].mean().reset_index(), x='When: Phase of flight', y='Feet above ground', title='Average Altitude by Phase of Flight',
                               color_discrete_sequence=['#FF6692'])

# Effect of bird strikes & impact on flight
effect_on_flight = px.bar(df['Effect: Impact to flight'].value_counts().reset_index(), x='index', y='Effect: Impact to flight',
                           title='Effect of Bird Strikes on Flight',
                           color_discrete_sequence=['#B6E880'])

# Effect of strike at different altitude
effect_at_altitude = px.box(df, x='Effect: Impact to flight', y='Feet above ground', title='Effect of Bird Strikes at Different Altitudes',
                            color_discrete_sequence=['#FF97FF'])

# Were pilots informed? & Prior warning and effect of strike relation
# Create a pivot table to prepare the data for heatmap
pivot_df = df.pivot_table(index='Effect: Impact to flight', columns='Pilot warned of birds or wildlife?', aggfunc='size', fill_value=0)

# Plot the heatmap
pilot_informed_warning = px.imshow(pivot_df, 
                                   labels=dict(x="Pilot Warned of Birds or Wildlife?", y="Effect of Bird Strikes", color="Count"),
                                   x=pivot_df.columns,
                                   y=pivot_df.index,
                                   title="Effect of Bird Strikes with Pilot Information",
                                   color_continuous_scale='Viridis')

# Step 3: Load - Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 4: Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Bird Strikes Analysis Dashboard"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='yearly-analysis', figure=yearly_line_chart)),
        dbc.Col(dcc.Graph(id='top-airlines', figure=top_airlines)),
        dbc.Col(dcc.Graph(id='top-airports', figure=top_airports)),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='yearly-cost', figure=yearly_cost)),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='altitude-at-strike', figure=altitude_at_strike)),
        dbc.Col(dcc.Graph(id='flight-phase-at-strike', figure=flight_phase_at_strike)),
        dbc.Col(dcc.Graph(id='avg-altitude-by-phase', figure=avg_altitude_by_phase)),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='effect-on-flight', figure=effect_on_flight)),
    ]),

     dbc.Row([
        dbc.Col(dcc.Graph(id='effect-at-altitude', figure=effect_at_altitude)),
        dbc.Col(dcc.Graph(id='pilot-informed-warning', figure=pilot_informed_warning)),
    ]),
])

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

