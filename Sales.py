import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

# Step 1: Extract - Load the dataset
# Assuming the dataset is in a CSV file named 'Amazon Sales data.csv'
df = pd.read_csv('Amazon Sales data.csv')

# Step 2: Transform - Analyze sales trends and compute key metrics
# Convert 'Order Date' column to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Extract year and month from 'Order Date' column
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Group by year and month to analyze month-wise sales trend
monthly_sales = df.groupby(['Year', 'Month'])['Total Revenue'].sum().reset_index()

# Group by year to analyze year-wise sales trend
yearly_sales = df.groupby('Year')['Total Revenue'].sum().reset_index()

# Group by year and month to analyze yearly-month-wise sales trend
yearly_monthly_sales = df.groupby(['Year', 'Month'])['Total Revenue'].sum().unstack()

# Compute key metrics
key_metrics = df.groupby(['Year', 'Month']).agg({
    'Total Revenue': 'sum',
    'Units Sold': 'sum',
    'Total Profit': 'sum',
    # Add more metrics as needed
}).reset_index()

# Additional Analysis
region_sales = df.groupby('Region')['Total Revenue'].sum().reset_index()
channel_sales = df.groupby('Sales Channel')['Total Revenue'].sum().reset_index()

# Step 3: Load - Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 4: Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Amazon Sales Dashboard"),
    
    # Graphs in a single row
    dbc.Row([
        # Month-wise sales trend plot
        dbc.Col(
            dcc.Graph(id='month-wise-sales',
                      figure=px.line(monthly_sales, x='Month', y='Total Revenue', 
                                     color='Year', title='Month-wise Sales Trend')),
            width=6
        ),
        
        # Year-wise sales trend plot
        dbc.Col(
            dcc.Graph(id='year-wise-sales',
                      figure=px.bar(yearly_sales, x='Year', y='Total Revenue', 
                                    title='Year-wise Sales Trend', labels={'Year': 'Year', 'Total Revenue': 'Revenue'}, color_discrete_sequence=['magenta'])),
            width=6
        )
    ]),
    
    # Yearly-monthly sales trend heatmap
    html.Div(
        dcc.Graph(id='yearly-monthly-sales',
                  figure=px.imshow(yearly_monthly_sales, 
                                   labels=dict(x="Month", y="Year", color="Total Revenue"),
                                   x=yearly_monthly_sales.columns, y=yearly_monthly_sales.index,
                                   title='Yearly-Monthly Sales Trend')),
    ),
    
    # Key metrics table
    html.H2("Key Metrics"),
    dcc.Graph(id='key-metrics',
              figure=px.bar(key_metrics, x='Month', y='Total Revenue', 
                            title='Monthly Sales Metrics', color_discrete_sequence=['green'])),
    
    # Additional Analysis
    dbc.Row([
        # Region-wise sales distribution
        dbc.Col(
            dcc.Graph(id='region-sales',
                      figure=px.bar(region_sales, x='Region', y='Total Revenue', 
                                    title='Region-wise Sales Distribution', color_discrete_sequence=['cyan'])),
            width=6
        ),
        
        # Sales channel distribution
        dbc.Col(
            dcc.Graph(id='channel-sales',
                      figure=px.bar(channel_sales, x='Sales Channel', y='Total Revenue', 
                                    title='Sales Channel Distribution', color_discrete_sequence=['orange'])),
            width=6
        )
    ]),
])

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

