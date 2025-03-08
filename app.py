import requests
import pandas as pd
from dash import Dash, html, dcc, callback, Input, Output, dash_table, callback_context
from scraping_tools import scrape_delegate, json_delegate



app = Dash()


app.layout = html.Div(children=[
    html.H1('Nyhedsaggregator'),
    html.Div(children=[

        html.Div(children=[

            html.Label('Søgetermer'),
            dcc.Input(value='',type='text', id='termer')
        ], style={'display': 'inline-block'}),

        html.Div(children=[

            html.Label('Agenturer'),
            dcc.Dropdown(options=['Jyllands Posten', 'TV2', 'Ekstra Bladet'], value=None,multi=True,id='bureauer',style={'display': 'inline-block'})
        ]),

        html.Div(children=[
            
            html.Button('Søg', id='søg',n_clicks=0)
        ])], 
        style={}),

    html.Div(id='container')

], style = {})

def create_children(as_JSON):
    titel = as_JSON['Title']
    tid = as_JSON['Time']
    link = as_JSON['Link']
    layout = [
        html.Div(titel, style={'font-weight':'bold','display': 'inline-block','padding-right':'2px'}),
        html.Div(tid, style={'display': 'inline-block','padding':'2px'}),
        dcc.Link(titel,href=link,style={'padding-left':'2px'})
    ]
    return layout

@callback(
    #Output = Siderne i al deres pragt
    Output(component_id='container',component_property='children'),
    #Inputs = Siderne og termerne plus knappen
    Input(component_id='bureauer', component_property='value'),
    Input(component_id='termer', component_property='value'),
    Input(component_id='søg', component_property='n_clicks')
)
def search_news(bureauer,termer,clicks):
    children = []
    if callback_context.triggered_id == 'søg':
        for bureau in bureauer:
            children.append(html.H3(bureau))
            articles = scrape_delegate(bureau,termer)
            for article in articles:
                as_JSON = json_delegate(bureau)(article)
                children.append(html.Div(create_children(as_JSON)))
    return children

app.run(debug=True)