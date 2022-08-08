import requests as rq
import bs4
import dash
import  dash_core_components as dcc
import  dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import os
## Define the app
app = dash.Dash(__name__)


## Read in our data
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
    "value"   : "volume", 
    "variable" : "level"})


## Produce the figure
gdp1=gdp.loc[(gdp.level=='IMF_Estimate')]

gdp2=gdp.loc[(gdp.level=='UN_Estimate')]

gdp3=gdp.loc[(gdp.level=='WB_Estimate')]



## This creates the layout of the page
app = dash.Dash(__name__)

## Produce the figure
fig = px.bar(gdp1, x = "Region", y = "volume", color = "Country")
## This creates the layout of the page
app.layout = html.Div(children=[
    ## HTML elements added with html.method
    html.H1(children='GDP by country'),
    
    ## Dynamic graph is added with dcc.METHOD (dcc = dynamic core component)
    dcc.Graph(
        id = 'graph',
        figure = fig
    )
])

## Produce the figure
fig = px.bar(gdp2, x = "Region", y = "volume", color = "Country")
## This creates the layout of the page
app.layout = html.Div(children=[
    ## HTML elements added with html.method
    html.H1(children='GDP by country'),
    
    ## Dynamic graph is added with dcc.METHOD (dcc = dynamic core component)
    dcc.Graph(
        id = 'graph',
        figure = fig
    )
])
## Produce the figure
fig = px.bar(gdp3, x = "Region", y = "volume", color = "Country")
## This creates the layout of the page
app.layout = html.Div(children=[
    ## HTML elements added with html.method
    html.H1(children='GDP by country'),
    
    ## Dynamic graph is added with dcc.METHOD (dcc = dynamic core component)
    dcc.Graph(
        id = 'graph',
        figure = fig
    )
])

## This runs the server
if __name__ == '__main__':
    app.run_server(debug=False, host = 'jupyter.biostat.jhsph.edu', port=os.getuid()+25)
