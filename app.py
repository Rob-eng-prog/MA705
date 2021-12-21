#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


robelhagos
"""

import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px



stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table

def generate_table(dataframe, max_rows=11):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app = dash.Dash(__name__, external_stylesheets=stylesheet)

CO2_df  = pd.read_csv("CO2_Dataset.csv")
first_decade = CO2_df.loc[0:10]
second_decade = CO2_df.loc[11:20]
third_decade = CO2_df.loc[21:30]
fourth_decade = CO2_df.loc[31:40]

def df_matcher(x):
    if x == '1':
        return first_decade
    elif x == '2':
        return second_decade
    elif x == '3':
        return third_decade
    else:
        return fourth_decade
#fig = px.bar(CO2_df,x="Africa Carbon Emission",y="Year")



app.layout = html.Div([html.H1("Carbon Dioxide Emission: United States Vs Africa", style={'color': 'blue'}),
                       html.H2("A story of how one country's CO2 emission compares to an enitre continent's", style={'color': 'blue'}),
                       html.P("In this dashboard, we will see how the carbon dioxide emission of the United States (one country) compares to that of Africa (a whole continent)."),
                       html.P("On the table below, we can see the total CO2 emission by Africa and U.S every year from 1980-2020 in tonnes."),
                       html.P("We will also see how the population of U.S compares to the entire continent of Africa (Africa has 54 countries)."),
                       html.P("The main goal of this dashboard is to show how one country emits way more C02 compared to an entire continent despite having less population, leading to both suffering the same consequences -Global Warming."),
                       html.P("Cilck on the drop down menu and choose a decade to see how the carbon dioxide emission of the U.S compares to that of Africa in each year of that decade in tonnes."),
                       html.P("The annual mean carbon dioxide part per million (PPM) is also given in the table below."),
                       html.P("Carbon dioxide part per million (PPM) is the number of particles of carbon dioxide per one million particles of air."),
                       html.P("The more carbon dioxide is emitted, the more the carbon dioxide part per million which causes a rise in the earth's temperature ('Global Warming')."),
                       html.H6("choose a decade below: "),
                       dcc.Dropdown(
                           id='my_dropdown',
                           options=[
                        {'label': '1980-1990', 'value': '1'},
                        {'label': '1991-2000', 'value': '2'},
                        {'label': '2001-2010', 'value': '3'},
                        {'label': '2011-2020', 'value':'4'},
                        ],
                        value='first_decade'
                        ),
                      html.H3("Table:"),
                       html.Div(id="output_box"),
                       html.H3("How does the population of the U.S compares to that of Africa over the decades?"),
                       html.H6("choose a decade below: "),
                       dcc.Dropdown(
                           id='my_dropdown0',
                           options=[
                        {'label': '1980-1990', 'value': '1'},
                        {'label': '1991-2000', 'value': '2'},
                        {'label': '2001-2010', 'value': '3'},
                        {'label': '2011-2020', 'value':'4'},
                        ],
                        value='first_decade'
                        ),
                       dcc.Graph(id='barplot0'),
                      
                       html.H4("How does the carbon dioxide emission of the U.S compares to that of Africa throughout the years?"),
                       html.H6("choose a decade below: "),
                       dcc.Dropdown(
                           id='my_dropdown1',
                           options=[
                        {'label': '1980-1990', 'value': '1'},
                        {'label': '1991-2000', 'value': '2'},
                        {'label': '2001-2010', 'value': '3'},
                        {'label': '2011-2020', 'value':'4'},
                        ],
                        value='first_decade'
                        ),
                       dcc.Graph(id='barplot'),
                       html.H5("Takeaway- The U.S emits way more CO2 than the entire African continent despite having lesser population.", style={'color': 'red'}),
                       
                       html.H4("How did the global annual CO2 PPM change over the decades?"),
                       html.H6("choose a decade below: "),
                       dcc.Dropdown(
                           id='my_dropdown2',
                           options=[
                        {'label': '1980-1990', 'value': '1'},
                        {'label': '1991-2000', 'value': '2'},
                        {'label': '2001-2010', 'value': '3'},
                        {'label': '2011-2020', 'value':'4'},
                        ],
                        value='first_decade'
                        ),
                       dcc.Graph(id='timeplot'),
                       html.H5("Takeaway- The global PPM has been increasing since 1980 and we are at a high risk of increased global temperature more than ever.", style={'color': 'red'}),
                       html.H3("References"),
                       html.A("Reference for data about carbon dioxide emission",
                            href="https://ourworldindata.org/co2-emissions",
                              target= "_blank"),
                       html.Br(),
                       html.A("Reference for data about global annual mean carbon ppm",
                              href="https://gml.noaa.gov/ccgg/trends/data.html",
                              target = "_blank"),
                       html.Br(),
                       html.A("Reference for data about U.S population",
                              href="https://www.macrotrends.net/countries/USA/united-states/population",
                              target = "_blank"),
                       html.Br(),
                       html.A("Reference for data about the poulation of Africa",
                              href="https://www.macrotrends.net/countries/AFR/africa/population",
                              target = "_blank")
                       
                       ])


server = app.server
@app.callback(
    Output(component_id="output_box",component_property="children"),
    [Input(component_id="my_dropdown",component_property="value")]
    )
def selected_table(value):
    return (generate_table(df_matcher(value)))

@app.callback(
    Output(component_id="barplot",component_property="figure"),
    [Input(component_id="my_dropdown1",component_property="value")]
    )
    
def selected_barplots(value):
    fig = px.bar(df_matcher(value),x="Year",y=["Africa Carbon Emission (tonnes)","U.S Carbon Emission (tonnes)"],title="CO2 emission (in billion tonnes) of U.S vs Africa over the years.", barmode="group",
                 labels = {'["Africa Carbon Emission (tonnes)","U.S Carbon Emission (tonnes)"]':'Carbon dioxide Emission (tonnes)'})
    return fig

@app.callback(
    Output(component_id="timeplot",component_property="figure"),
    [Input(component_id="my_dropdown2",component_property="value")]
    )
    
def selected_timeplot(value):
      fig =  px.line(df_matcher(value),x='Year',y='Annual Mean CO2 (PPM)',title="Annual Mean CO2 PPM throughout the decades")
      return fig

@app.callback(
    Output(component_id="barplot0",component_property="figure"),
    [Input(component_id="my_dropdown0",component_property="value")]
    )

def selected_barplots_population(value):
    fig = px.bar(df_matcher(value),x="Year",y=["Africa Population (Millions)", "U.S Population (Millions)"],title="Population (in billions) of U.S vs Africa over the years", barmode="group")
    return fig

    
if __name__ == '__main__':
    app.run_server(debug=True)
    


