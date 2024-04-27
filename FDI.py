import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

# Step 1: Extract - Load the dataset
fdi_df = pd.read_csv('FDI data.csv')

# Step 2: Transform - Analyze FDI trends and compute key metrics

# Get the latest year data
latest_year = fdi_df.columns[-1]  # Assuming the last column is the latest year
latest_year_data = fdi_df[['Sector', latest_year]]

# Sector-wise investment analysis for the latest year
sector_wise_investment_latest_year = latest_year_data.groupby('Sector').sum().reset_index()

# Year-wise investment
yearly_investment = fdi_df.sum()[1:]

# Aggregate sectors with less than 1% into 'Others' for pie chart
sector_wise_investment_latest_year_pie = latest_year_data.groupby('Sector').sum().reset_index()
total_investment = sector_wise_investment_latest_year_pie[latest_year].sum()
sector_wise_investment_latest_year_pie['Percentage'] = sector_wise_investment_latest_year_pie[latest_year] / total_investment
others_threshold = 0.01
filtered_sectors = sector_wise_investment_latest_year_pie[sector_wise_investment_latest_year_pie['Percentage'] >= others_threshold]['Sector']
sector_wise_investment_latest_year_pie.loc[~sector_wise_investment_latest_year_pie['Sector'].isin(filtered_sectors), 'Sector'] = 'Others'
sector_wise_investment_latest_year_pie = sector_wise_investment_latest_year_pie.groupby('Sector').sum().reset_index()

# Step 3: Load - Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 4: Define the layout of the dashboard
app.layout = html.Div([
    html.H1("FDI Analysis Dashboard"),
    
    # Sector-wise investment analysis plot for the latest year
    html.Div([
        dcc.Graph(id='sector-wise-investment-latest-year',
                  figure=px.bar(sector_wise_investment_latest_year, x='Sector', y=latest_year,
                                title=f'Sector-wise FDI Analysis for {latest_year}', 
                                color_discrete_sequence=['blue']).update_layout(height=1000, margin=dict(l=40, r=40, t=40, b=40), showlegend=True).update_yaxes(title_text='FDI in USD for 2016-17')
                 ),
    ]),

    # Pie chart showing distribution of FDI across sectors for the latest year
    html.Div([
        dcc.Graph(id='sector-pie-chart',
                  figure=px.pie(sector_wise_investment_latest_year_pie, values=latest_year, names='Sector',
                                title=f'Sector-wise FDI Distribution for {latest_year}')
                 ),
    ]),

    # Line chart showing trend of FDI across years
    html.Div([
        dcc.Graph(id='yearly-trend',
                  figure=px.line(x=yearly_investment.index, y=yearly_investment.values,
                                 title='Yearly FDI Trend').update_layout(height=400, margin=dict(l=40, r=40, t=40, b=40), showlegend=True).update_xaxes(title_text='Year').update_yaxes(title_text='Total FDI across all sectors (USD)')
                 ),
    ]),
])

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

