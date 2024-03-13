import taipy as tp
import numpy as np
import taipy.gui.builder as tgb
from taipy.gui import Gui, Markdown
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

file_path = 'data_agric/Asia_Production_Crops_Livestock.csv'
    
# Read the CSV file
data = pd.read_csv(file_path)

# Function to format large numbers with abbreviations
def human_readable_numbers(value):
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(value) < 1000:
            return f"{value:3.1f}{unit}"
        value /= 1000
    return f"{value:3.1f}Y"

# Function to format large numbers with full words
def human_readable_full(value):
    if value < 1000:
        return str(value)
    elif 1000 <= value < 1e6:
        return f"{value / 1000:.2f} Thousand"
    elif 1e6 <= value < 1e9:
        return f"{value / 1e6:.2f} Million"
    elif 1e9 <= value < 1e12:
        return f"{value / 1e9:.2f} Billion"
    elif 1e12 <= value < 1e15:
        return f"{value / 1e12:.2f} Trillion"
    else:
        return f"{value / 1e15:.2f} Quadrillion"

custom_color_scale = [
    [1.0, 'rgb(137, 174, 255)'],     # for very large values
    [0.5, 'rgb(118, 161, 255)'],     # for large values
    [0.1, 'rgb(98, 148, 255)'],      # for medium-large values
    [0.01, 'rgb(81, 136, 255)'],     # for medium values
    [1e-3, 'rgb(66, 126, 255)'],     # for medium-small values
    [1e-6, 'rgb(52, 116, 255)'],     # for small values
    [1e-9, 'rgb(32, 103, 255)'],     # for very small values
    [0, 'rgb(0, 81, 255)'],          # for the lowest value
]

# Updated create_production_by_continent_map function
def create_production_by_country_map(data):
    # Group data by 'Country' and sum the 'Normalized Value' for production
    country_production = data[data['Element'] == 'Production'].groupby('Country')['Normalized Value'].sum().reset_index()
    # Create a choropleth map
    fig = px.choropleth(country_production, locations="Country", locationmode='country names',
                        color="Normalized Value", hover_name="Country", labels={'Country':'Country'},
                        hover_name="Country", hover_data=["Production", "Element"],  # Additional info in hover tooltip
                        animation_frame="Year",
                        title='Total Agricultural Production by Country in Asia', color_continuous_scale=custom_color_scale)
    fig.update_layout(geo=dict(scope='asia'),
                      title={'text': "Total Agricultural Production by Country in Asia", 'y': 0, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      autosize=True)  # Set autosize to True to fill container
    return fig

# Updated create_pie_figure function for other categories
def create_pie_fig(data, group_by: str, threshold=0.01):
    # Group data by the specified column and sum the 'Normalized Value'
    grouped_data = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    grouped_data['Readable Value'] = grouped_data['Normalized Value'].apply(human_readable_full)

    # Create the pie chart with the filtered data
    fig = px.pie(grouped_data, names='Item Category', values='Normalized Value', title=f"Total Production by {group_by}", hole=0.2,
                 hover_data=['Readable Value'])
    fig.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, height= 800)
    fig.update_traces(textinfo='percent+label')
    return fig

def create_pie_fig_element(data, group_by: str, threshold=0.01):
    # Group data by the specified column and sum the 'Normalized Value'
    grouped_data = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    grouped_data['Readable Value'] = grouped_data['Normalized Value'].apply(human_readable_full)

    # Create the pie chart with the filtered data
    fig = px.pie(grouped_data, names='Element', values='Normalized Value', title=f"Total Production by {group_by}", hole=0.2,
                 hover_data=['Readable Value'])
    fig.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, height= 800)
    fig.update_traces(textinfo='percent+label')
    return fig

# Updated create_pie_figure function for countries
def create_pie_fig_country(data, group_by: str, threshold=0.01):
    # Group data by the specified column and sum the 'Normalized Value'
    grouped_data = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    grouped_data['Readable Value'] = grouped_data['Normalized Value'].apply(human_readable_full)
    
    # Group small categories into 'Rest'
    total_value = grouped_data['Normalized Value'].sum()
    grouped_data['Country'] = grouped_data.apply(lambda row: row[group_by] if row['Normalized Value'] / total_value >= threshold else 'Rest', axis=1)
    final_data = grouped_data.groupby('Country')[['Normalized Value', 'Readable Value']].sum().reset_index()

    # Create the pie chart with the filtered data
    fig = px.pie(final_data, names='Country', values='Normalized Value', title=f"Total Production by {group_by}", hole=0.2,
                 hover_data=['Readable Value'])
    fig.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, height=600)
    fig.update_traces(textinfo='percent+label')
    return fig

# Updated create_bar_figure function
def create_bar_fig(data, group_by: str):
    # Group data by the specified column and sum the 'Normalized Value'
    production_over_time = data.groupby(group_by)['Normalized Value'].sum().reset_index()
    # Create a bar chart
    fig = px.bar(production_over_time, x=group_by, y='Normalized Value', title=f'Production Trends Over Time by {group_by}', color='Normalized Value')
    # Calculate the tick values and labels
    max_value = production_over_time['Normalized Value'].max()
    tick_values = np.linspace(0, max_value, num=5)  # Adjust num for the number of ticks you want
    tick_labels = [human_readable_full(v) for v in tick_values]
    
    # Update y-axis with custom tick labels
    fig.update_layout(yaxis=dict(tickvals=tick_values, ticktext=tick_labels), yaxis_title='Production Total (Normalized)', yaxis_automargin=True, title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig

def create_perc_other_fig(data, group_by: str, threshold=1):
    # Group, sum, and convert to percentage
    grouped_data = data.groupby(['Year', group_by])['Normalized Value'].sum().unstack(fill_value=0)
    percentages = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
    percentages = percentages.round(3)  # Round to 3float numbers

    # Flatten the DataFrame and reset index
    percentages = percentages.stack().reset_index(name='Percentage')
    
    # Group small categories into 'Other'
    small_categories_mask = percentages['Percentage'] < threshold
    percentages.loc[small_categories_mask, group_by] = 'Rest'
    
    # Sum the 'Other' categories
    final_data = percentages.groupby(['Year', group_by])['Percentage'].sum().reset_index()

    # Create the initial figure using plotly.express
    fig = px.bar(final_data, x='Year', y='Percentage', color=group_by,
                 title=f"Evolution of Agriculture Production by {group_by} over Time",
                 labels={'Percentage': 'Percentage(%) of Production'}, text=None)
    
    # Calculate the average percentage for each group across all years
    average_percentages = final_data.groupby(group_by)['Percentage'].mean().reset_index()

    # Modify the trace names to include the average percentage values
    for trace in fig.data:
        group_name = trace.name
        average_percentage = average_percentages[average_percentages[group_by] == group_name]['Percentage'].iloc[0]
        trace.name = f"{group_name} {average_percentage:.3f}%"

    # Update the layout to stack the bars and set the height
    fig.update_layout(barmode='stack',title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, height=500)
    return fig

def create_perc_fig(data, group_by: str):
    # Group, sum, and convert to percentage
    grouped_data = data.groupby(['Year', group_by])['Normalized Value'].sum().unstack(fill_value=0)
    percentages = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
    percentages = percentages.round(3)  # Round to 3 float numbers

    # Flatten the DataFrame and reset index
    percentages = percentages.stack().reset_index(name='Percentage')
    
    # Sum the categories
    final_data = percentages.groupby(['Year', group_by])['Percentage'].sum().reset_index()
    
    # Create the initial figure using plotly.express
    fig = px.bar(final_data, x='Year', y='Percentage', color=group_by,
                 title=f"Evolution of Agriculture Production by {group_by} over Time",
                 labels={'Percentage': 'Percentage(%) of Production'}, text=None)

    # Calculate the average percentage for each group across all years
    average_percentages = final_data.groupby(group_by)['Percentage'].mean().reset_index()

    # Modify the trace names to include the average percentage values
    for trace in fig.data:
        group_name = trace.name
        average_percentage = average_percentages[average_percentages[group_by] == group_name]['Percentage'].iloc[0]
        trace.name = f"{group_name} {average_percentage:.3f}%"

    # Update the layout to stack the bars
    fig.update_layout(barmode='stack', title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, height=500)
    return fig


# Create figures
fig_item_category = create_pie_fig(data, 'Item Category')
fig_element = create_pie_fig_element(data, 'Element')
fig_country = create_pie_fig_country(data, 'Country')
fig_year = create_bar_fig(data, 'Year')

fig_map = create_production_by_country_map(data)


# list of Asian countries obtained from a reliable source.
asian_countries = [
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan",
    "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia",
    "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait",
    "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia",
    "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine",
    "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea",
    "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste",
    "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"
]

# Function to handle the on_change event and update visualizations.
filtered_data = data.loc[
    data["Country"].isin(asian_countries)
]

fig_country_perc = create_perc_other_fig(filtered_data, 'Country')
fig_item_category_perc = create_perc_fig(filtered_data, 'Item Category')
fig_element_perc = create_perc_fig(filtered_data, 'Element')
fig_item_perc = create_perc_other_fig(filtered_data, 'Item')

def on_selector(state):
    filtered_data = state.data.loc[
        state.data["Country"].isin(state.asian_countries)
    ]

    state.fig_country_perc = create_perc_other_fig(filtered_data, 'Country')
    state.fig_item_category_perc = create_perc_fig(filtered_data, 'Item Category')
    state.fig_element_perc = create_perc_fig(filtered_data, 'Element')
    state.fig_item_perc = create_perc_other_fig(filtered_data, 'Item')


# Define the page content using Taipy Gui Builder
with tgb.Page() as page:
    tgb.toggle(theme= True)
    tgb.text("GrowthSeer", class_name="h1"),
    tgb.text("Total Agricultural Production by Country in Asia", class_name="h3"),

    tgb.chart(figure="{fig_mapp}"),
    tgb.chart(figure="{fig_country}"),
    with tgb.layout("1 1", gap="1rem"):
        tgb.chart(figure="{fig_item_category}"),
        tgb.chart(figure="{fig_element}"),

    # Taipy GUI selector for countries.
    tgb.selector(
        value="{asian_countries}",
        lov=asian_countries, # custom countries list above
        dropdown=True,
        multiple=True,
        label="Select countries",
        class_name="fullwidth",
        on_change=on_selector
    )

    tgb.text("Analysis of Agricultural Production in Asia", class_name="h3")
    with tgb.layout("1 1", gap="0.5rem"):
        tgb.chart(figure="{fig_country_perc}"),
        tgb.chart(figure="{fig_item_category_perc}"),
        tgb.chart(figure="{fig_element_perc}"),
        tgb.chart(figure="{fig_item_perc}"),

    tgb.chart(figure="{fig_year}")
    tgb.table("{data}")

css_file = "style.css"
stylekit = {
    "color_primary": "rgb(127, 75, 182)", # Primary color used in elements.
    "color_secondary": "rgb(222, 191, 255)", # Accent color used to make elements stand out from others.
    "color_background_light": "rgb(248, 217, 217)", # Background color for the light theme.
    "color_background_dark": "rgb(43, 15, 58)", # Background color for the dark theme.
    "color_paper_dark": "rgb(85, 34, 113)", # Elevated elements (i.e. card, header, sidebar…) background color for the dark theme.
    "color_paper_light": "rgb(231, 206, 206)", # Elevated elements (i.e. card, header, sidebar…) background color for the light theme.
    "font_family": "'PT Sans', sans-serif",
    "border_radius": "21px",
    "color-contrast-dark": "rgb(248, 217, 217)", # Contrasting elements (such as text) color for dark backgrounds
    "color-contrast-light": "rgb(43, 15, 58)", # Contrasting elements (such as text) color for light backgrounds
    "font-size-h1": "3.5rem",
    "font-size-h2": "2rem",
    "font-size-h3": "1.6rem",
    "font-size-h4": "1.5rem",
    "font-size-body": "1.5rem",
    "custom-scrollbar-thumb-color-dark": "rgb(222, 191, 255)", # Light purple for thumb on dark theme
    "custom-scrollbar-rail-color-dark": "rgb(85, 34, 113)",    # Dark purple for rail on dark theme
    "custom-scrollbar-thumb-color-light": "rgb(127, 75, 182)", # Dark purple for thumb on light theme
    "custom-scrollbar-rail-color-light": "rgb(231, 206, 206)",  # Light pink for rail on light theme
}
# Create the GUI instance
gui = Gui(page=page, css_file=css_file)

# Run the app
if __name__ == "__main__":
    gui.run(title="GrowthSeer: Agricultural data dashboard",stylekit=stylekit, port=3000)