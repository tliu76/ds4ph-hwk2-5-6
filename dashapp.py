import requests as rq
import bs4
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import os
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
page = rq.get(url)
## print out the first 200 characters just to see what it looks like
page.text[0 : 99]

bs4page = bs4.BeautifulSoup(page.text, 'html.parser')
tables = bs4page.find('table',{'class':"wikitable"})

gdp = pd.read_html(str(tables))

gdp = pd.read_html(str(tables), header=[1])[0]
gdp.columns=["Country","Region","IMF_Estimate","IMF_Year","UN_Estimate","UN_Year","WB_Estimate","WB_Year"]
gdp.drop(["IMF_Year","UN_Year","WB_Year"], axis = 1)
gdp = gdp.melt(id_vars=["Country", "Region"])
gdp=gdp.rename(columns = {
    "value"   : "gdp", 
    "variable" : "level"})


app.layout = html.Div([
    dcc.Dropdown(options = [
            {'label' :'WB_Estimate', 'value' : 'WB_Estimate'},
            {'label' : 'UN_Estimate', 'value' : 'UN_Estimate'},
            {'label' : 'IMF_Estimate', 'value' : 'IMF_Estimate'}
        ],value = 2,
   id = 'input-level' ),
    dcc.Graph(id = 'output-graph')
])

@app.callback(
    Output('output-graph', 'figure'),
    Input('input-level', 'value'))
def update_figure(selected_level):
    subdat = gdp.loc[gdp['level'] == selected_level].sort_values(by = ['gdp'])
    fig = px.bar(subdat, x='Region', y='gdp',color='Country')
    return fig

if __name__ == '__main__':
      app.run_server(debug=False, host = 'jupyter.biostat.jhsph.edu', port=os.getuid()+15)

