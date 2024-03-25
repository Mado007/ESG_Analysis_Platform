import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import plot
from flask import render_template

# Correctly set up the directory to where your CSV files are stored
data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Function to safely load CSV files
def safely_load_csv(filename):
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        return pd.read_csv(path, on_bad_lines='skip')
    else:
        print(f"File not found: {path}")
        return pd.DataFrame()  # Return an empty DataFrame if file doesn't exist

# Load the CSV files into Pandas DataFrames using the safeguard function
esg_data_df = safely_load_csv('ESGData.csv')
# esg_country_series_df = safely_load_csv('ESGCountry-Series.csv')
# esg_country_df = safely_load_csv('ESGCountry.csv')
# esg_footnote_df = safely_load_csv('ESGFootNote.csv')
# esg_series_time_df = safely_load_csv('ESGSeries-Time.csv')

# Utility function to clean data
def clean_esg_data(dataframe):
    return dataframe.dropna(subset=['Indicator Name', 'Country Code'])

# Example utility for generating a Plotly figure
def generate_plotly_figure(dataframe):
    indicator_name = "Access to electricity (% of population)"
    country_code = "ARB"  # Example Country Code
    
    df_filtered = dataframe[(dataframe['Indicator Name'] == indicator_name) &
                            (dataframe['Country Code'] == country_code)]
    df_filtered = df_filtered.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                                   var_name='Year', value_name='Percentage')
    df_filtered = df_filtered.dropna(subset=['Percentage'])
    df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
    
    # Create Plotly figure
    fig = px.line(df_filtered, x='Year', y='Percentage',
                  title=f'{indicator_name} - {country_code}')
    return fig

# Use previously defined functions for data loading and cleaning
esg_data_cleaned = clean_esg_data(esg_data_df)

# Generate Plotly figure
fig = generate_plotly_figure(esg_data_cleaned)
    
# Save Plotly figure as HTML
# plot(fig, filename=os.path.join(data_dir, 'dashboard.html'))
