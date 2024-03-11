import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import plotly.express as px

file_path = 'data/Asia_Production_Crops_Livestock.csv'
    
# Read the CSV file
data = pd.read_csv(file_path)

# Function to format large numbers in a more readable way
def human_readable_numbers(value):
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(value) < 1000:
            return f"{value:3.1f}{unit}"
        value /= 1000
    return f"{value:3.1f}Y"

# Updated create_pie_figure function
def create_pie_figure(data, group_by: str, threshold=0.01):
    # Group data by the specified column and sum the 'Normalized Value'
    grouped_data = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    grouped_data['Normalized Value'] = grouped_data['Normalized Value'].round(2)
    
    # Group small categories into 'Other'
    total_value = grouped_data['Normalized Value'].sum()
    grouped_data['Category'] = grouped_data.apply(lambda row: row[group_by] if row['Normalized Value'] / total_value >= threshold else 'Other', axis=1)
    final_data = grouped_data.groupby('Category')['Normalized Value'].sum().reset_index()

    # Create the pie chart with the filtered data
    fig = px.pie(final_data, names='Category', values='Normalized Value', title=f"Total Production by {group_by}", hole=0.3)
    fig.update_traces(textinfo='percent+label')
    return fig

# Updated create_bar_figure function
def create_bar_figure(data, group_by: str):
    # Group data by the specified column and sum the 'Normalized Value'
    production_over_time = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    # Create a bar chart
    fig = px.bar(production_over_time, x=group_by, y='Normalized Value', title=f'Production Trends Over Time by {group_by}', color='Normalized Value')
    # Update y-axis to use human-readable numbers
    fig.update_layout(yaxis_tickformat = ',')
    return fig

# Updated create_production_by_continent_map function
def create_production_by_continent_map(data):
    # Group data by 'Country' and sum the 'Normalized Value' for production
    country_production = data[data['Element'] == 'Production'].groupby('Country')['Normalized Value'].sum().reset_index()
    # Create a choropleth map
    fig = px.choropleth(country_production, locations="Country", locationmode='country names',
                        color="Normalized Value", hover_name="Country", text="Country",
                        title='Total Agricultural Production by Country in Asia',
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(geo=dict(scope='asia'),
                      title={'text': "Total Agricultural Production by Country in Asia", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(textposition='top center')
    return fig

# Create figures

fig_map = create_production_by_continent_map(data)
fig_item = create_pie_figure(data, 'Item Category')
fig_country = create_pie_figure(data, 'Country')

fig_year = create_bar_figure(data, 'Year')

# Define the page content using Taipy Gui Builder
with tgb.Page() as page:
    tgb.text("Agriculture Data Analysis App", class_name="h1"),

    tgb.chart(figure="{fig_map}"),

    tgb.chart(figure="{fig_item}"),
    tgb.chart(figure="{fig_country}")

    tgb.chart(figure="{fig_year}")
    tgb.table("{data}")
# Create the GUI instance
gui = Gui(page=page)

# Run the app
if __name__ == "__main__":
    gui.run(title="Agriculture Data Analysis App", port=3000)