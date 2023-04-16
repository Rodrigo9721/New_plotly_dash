import os
import pandas as pd
import numpy as np
import pickle
from dash import Dash, dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_daq as daq
import json
import platform
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import geopandas as gpd
import pathlib
from data import data, create_dropdown_options
from pages import search, interact
from pages.search import update_output_search
#from pages.interact import table_interactions, create_layout
pd.options.mode.chained_assignment = None

app = Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)
server = app.server

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

## Data
db = pd.read_csv('unica.csv', encoding='latin-1')
db2 = pd.read_csv('anualizada.csv', encoding='latin-1')
db, db2 = data(db, db2)
full_table = db[['ENTIDAD', 'REGIÓN', 'PROVINCIA', 'RUC_ENTIDAD']].sort_values(by=['REGIÓN', 'PROVINCIA'], ascending=True)



## Data

ENTORNO = 'desarrollo' if 'windows' in platform.platform().lower() else 'production'
CG_LOGO = '/assets/Credigob-Logo.jpg'

# Elementos


options_region, options_provincia = create_dropdown_options(db)

dropdown_region = dcc.Dropdown(
   options = options_region,
   value='',
   placeholder='Región',
   id = 'region',
   disabled=False
)
dropdown_provincia = dcc.Dropdown(
   options = options_provincia,
   value ='',
   placeholder ='Provincia',
   id = 'provincia',
   disabled=True
)

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Nombre o RUC", id='my-input', value='', debounce=True,
                          n_submit=0)),
        dbc.Col(
            dbc.Button("Buscar", color="secondary", class_name="button search", n_clicks=0, id='Button'),
            width="auto",
        ),
    ],
    class_name="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=CG_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Entidades del Estado", className="ms-2")) 
                    ],
                    align='center',
                    class_name='g-0'
                ),
                href="https://www.credigob.pe/",
                style={"textDecoration": "none", 'align':'left'},                
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),            
        ],
        class_name='a'
    ),
    color="rgb(109,126,125)",
    dark=True,
    className='search'
)

search = html.Div([
    dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=True,
                navbar=True,
            ),
    
])

table = dash_table.DataTable(
                id = 'Entities',
                columns=[
                    {"name": i, "id": i, "selectable": True} for i in full_table.columns
                ],
                data = full_table.to_dict('records'),
                row_selectable='single',
                selected_rows=[],
                style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px',
                                'text-align':'left'
                            },
                            style_cell={
                                'text-align':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)',
                                'textAlign':'left'}           
            )

# Elementos


# Layout

def create_layout(app):
    return html.Div([
        navbar,
        html.Br(),
        dbc.Row([
            dbc.Col(dropdown_region, class_name='pos', id='Dropdown_R'),
            dbc.Col(dropdown_provincia, class_name='pos', id='Dropdown_P'),
            dbc.Col(search, class_name='pos')
            
        ], class_name='rows'),
        html.Div([
            html.H4('Entidades del Estado', className='pos'),
            html.Div([dbc.Row([
                dbc.Col(html.P('Seleccione la Entidad que está buscando', className='pos')),
                dbc.Col(html.Button('Volver', id='reset', n_clicks=0, className='button-1 reset'))
                ])             
            ]),
            
            html.Div([
                table
            ],className='content-table', id='content')
        ])


    ], id='body', className='main')

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash":
        return create_layout(app)


@app.callback(
    [Output(component_id='content', component_property='children'),
    Output(component_id='Dropdown_P', component_property='children'),
    Output(component_id='Dropdown_R', component_property='children'),
    Output(component_id='reset', component_property='n_clicks')],
     [Input(component_id='provincia', component_property='value'),
      Input(component_id='region', component_property='value'),
      Input(component_id='my-input', component_property='value'),
      Input(component_id='Button', component_property='n_clicks'),
      Input(component_id='my-input', component_property='n_submit'),
      Input(component_id='reset', component_property='n_clicks'),
      Input(component_id='region', component_property='disabled'),
      Input(component_id='Entities', component_property='selected_rows')
      ]
    )
def callback_search(provincia, region, input_value, n_clicks, n_submit, reset, disabled, selected_rows):
    return update_output_search(provincia, region, input_value, n_clicks, n_submit, reset, disabled, selected_rows)



#@app.callback(
#    [Output(component_id='content', component_property='children'),
#    Output(component_id='Dropdown_R', component_property='children')],
#     [Input(component_id='Entities', component_property='active_cell')]
#      )
#def callback_interact(active_cell):
#    return table_interactions(active_cell)





# Layout

PORT = int(os.environ.get("PORT", 8050))

if __name__ == '__main__':
    if (ENTORNO == 'desarrollo'):
        app.run_server(debug=True, port=PORT)
    else:
        app.run_server(debug=True, host='localhost', port=PORT)