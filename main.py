import taipy as tp
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from taipy.gui import Gui


data = pd.read_csv('data/Temperature-Change-on-Land.csv')

# Define the start and end years
start_year = 1961
end_year = 2022

# Initialize an empty list to store the button arguments
button_args_list = []

# Create button arguments for each year
for year in range(start_year, end_year + 1):
    button_args = dict(args=['Year', year], label=str(year), method='restyle')
    button_args_list.append(button_args)

# Construct the updatemenus dictionary
updatemenus = [
    dict(buttons=button_args_list,direction='down',pad={'r': 10, 't': 10},
        showactive=True,x=0.1,xanchor='left',y=1.1,yanchor='top')
]

def create_pie_figure(data, group_by: str):
    grouped_data = data.groupby(group_by)['Value'].sum().reset_index()
    grouped_data['Area'] = grouped_data['Area'].round(2)
    fig = px.pie(grouped_data, names=group_by, values='Value', title=f"temperature change by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by: str):
    temperature_over_time = data.groupby(group_by)['_id'].sum().reset_index()
    fig = px.bar(temperature_over_time, x=group_by, y='value', title='Temperature Trends Over Time', color='value')
    return fig

def create_change_by_country_map(data):
    temperature_change = data.groupby(['element', 'year']).agg({'value': 'sum'}).reset_index() 
    fig = px.scatter_geo(temperature_change, locationmode='country names', locations='_id', 
                        size='value', color='value', text='_id', hover_name='_id', projection='natural earth')
    fig.update_layout(title_text='Temperature Change by Country',title_x=0.5,updatemenus= updatemenus)
    return fig


fig_map = create_change_by_country_map(data)

#fig_temperture_change = create_pie_figure(temperature, 'value')

#fig_time = create_bar_figure(temperature, 'year')

with tgb.Page() as page:
    tgb.text("Tempareture Insights", class_name="h1")

    '''with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Total Sales", class_name="h2")
            tgb.text("{int(data['Total'].sum())}", class_name="h3")

        with tgb.part():
            tgb.text("Average Sales", class_name="h2")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")

        with tgb.part():
            tgb.text("Mean Rating", class_name="h2")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")'''

    tgb.chart(figure="{fig_map}")

    '''with tgb.layout("1 1 1"):
        tgb.chart(figure="{fig_product_line}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_customer_type}")
    
    tgb.chart(figure="{fig_time}")
    tgb.chart(figure="{fig_date}")

    tgb.text("Analysis", class_name="h2")

    tgb.selector(value="{city}", lov=["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"],
                 dropdown=True,
                 multiple=True,
                 label="Select cities",
                 class_name="fullwidth",
                 on_change=on_selector)

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_product_line_perc}")
        tgb.chart(figure="{fig_city_perc}")
        tgb.chart(figure="{fig_gender_perc}")
        tgb.chart(figure="{fig_customer_type_perc}")'''

    tgb.table("{temperature}")



if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Temperature on Land", port=3000)