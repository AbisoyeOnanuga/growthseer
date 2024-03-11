import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import plotly.express as px

file_path = 'data/Asia_Production_Crops_Livestock.csv'
    
# Read the CSV file
data = pd.read_csv(file_path)

def create_pie_figure(data, group_by: str):
    # Group data by the specified column and sum the 'Value'
    grouped_data = data.groupby(group_by)['Value'].sum().reset_index()
    grouped_data['Value'] = grouped_data['Value'].round(2)    # Set a threshold for grouping small categories into 'Other'

    # Create the pie chart with the filtered data
    fig = px.pie(grouped_data, names=group_by, values='Value', title=f"Total Production by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by: str):
    # Group data by the specified column and sum the 'Value'
    production_over_time = data.groupby(group_by)['Value'].sum().reset_index()
    # Create a bar chart
    fig = px.bar(production_over_time, x=group_by, y='Value', title=f'Production Trends Over Time by {group_by}', color='Value')
    return fig

def create_production_by_continent_map(data):
    # Assuming 'Latitude' and 'Longitude' columns are present in the data
    country_production = data[data['Element'] == 'Production'].groupby('Area')['Value'].sum().reset_index()
    # Create a scatter geo map
    fig = px.scatter_geo(country_production, locations="Area", locationmode='country names',
                         size="Value", color="Value", text="Area",
                         title='Total Agricultural Production by Country in Asia', size_max=100)
    fig.update_layout(geo=dict(scope='asia'),
                      title={'text': "Total Agricultural Production by Country in Asia", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
                      # Set a minimum size for bubbles (e.g., 10)
    fig.update_traces(marker=dict(sizemin=5))
    return fig

# Create figures

fig_map = create_production_by_continent_map(data)
fig_item = create_pie_figure(data, 'Item')
fig_country = create_pie_figure(data, 'Area')

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