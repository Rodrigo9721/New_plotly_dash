import os
import pandas as pd
import numpy as np
import pickle
from dash import Dash, dash_table, no_update
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_daq as daq
from data import data, create_dropdown_options, get_data_dash
import re
from unicodedata import normalize
pd.options.mode.chained_assignment = None


def update_output_search(provincia, region, input_value, n_clicks, n_submit, reset, disabled, selected_rows):
    db = pd.read_csv('unica.csv', encoding='latin-1')
    db2 = pd.read_csv('anualizada.csv', encoding='latin-1')
    db, db2 = data(db, db2)
    db = db.sort_values(by=['REGIÓN', 'PROVINCIA'], ascending=True)
    db.rename(columns={"%DEV-2021": "DEVENGADO"}, inplace=True)
    options_region, options_provincia = create_dropdown_options(db)
    full_table = db[['ENTIDAD', 'REGIÓN', 'PROVINCIA', 'RUC_ENTIDAD']]
    
    if reset > 0:
        table = dash_table.DataTable(
                            id = 'Entities',
                            columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                            row_selectable='single',
                            selected_rows=[],
                            data = full_table.to_dict('records'),
                            style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                        )
        dropdown_region = dcc.Dropdown(
            options = options_region,
            value = '',
            placeholder ='Región',
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
        return [table], [dropdown_provincia], [dropdown_region], 0
    if selected_rows == []:
        if region is None and disabled == False:
            if (input_value == '') and (n_clicks + n_submit == 0):
                table = dash_table.DataTable(
                            id = 'Entities',
                            columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                            row_selectable='single',
                            selected_rows=[],
                            data = full_table.to_dict('records'),
                            style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                        )

                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
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
                return [table], [dropdown_provincia], [dropdown_region], 0
            elif (input_value == '') and (n_clicks + n_submit > 0):

                table = dash_table.DataTable(
                            id = 'Entities',
                            columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                            row_selectable='single',
                            selected_rows=[],
                            data = full_table.to_dict('records'),
                            style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                        )
                
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
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
                return [table], [dropdown_provincia], [dropdown_region], 0
            elif (input_value != '') and (n_clicks + n_submit > 0):
                try:
                    is_int = int(input_value)
                    full_table['RUC_ENTIDAD'] = full_table['RUC_ENTIDAD'].astype(str)
                    full_table = full_table[full_table['RUC_ENTIDAD'].str.contains(input_value)]
                except:
                    input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                    input_value = normalize('NFC', input_value)
                    input_value = input_value.upper()
                    full_table = full_table[full_table['ENTIDAD'].str.contains(input_value)]
                table = dash_table.DataTable(
                            id = 'Entities',
                            columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                            row_selectable='single',
                            selected_rows=[],
                            data = full_table.to_dict('records'),
                            style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                        )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
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
                return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  == '') and (n_clicks + n_submit == 0):
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
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
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  == '') and (input_value == '') and (n_clicks + n_submit > 0):
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = '',
                    placeholder ='Región',
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
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  == '') and (input_value != '') and (n_clicks + n_submit > 0):
            try:
                is_int = int(input_value)
                full_table['RUC_ENTIDAD'] = full_table['RUC_ENTIDAD'].astype(str)
                full_table = full_table[full_table['RUC_ENTIDAD'].str.contains(input_value)]
            except:
                input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                input_value = normalize('NFC', input_value)
                input_value = input_value.upper()
                full_table = full_table[full_table['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
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
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (n_clicks + n_submit == 0):
            full_table2 = full_table[full_table['REGIÓN'] == region]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table2.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table2.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table2)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (input_value == '') and (n_clicks + n_submit > 0):
            full_table2 = full_table[full_table['REGIÓN'] == region]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table2.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table2.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table2)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (input_value != '') and (n_clicks + n_submit > 0):
            try:
                is_int = int(input_value)
                full_table2 = full_table[full_table['REGIÓN'] == region]
                options_region, options_provincia = create_dropdown_options(full_table2)
                full_table2['RUC_ENTIDAD'] = full_table2['RUC_ENTIDAD'].astype(str)
                full_table2 = full_table2[full_table2['RUC_ENTIDAD'].str.contains(input_value)]
            except:
                input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                input_value = normalize('NFC', input_value)
                input_value = input_value.upper()
                full_table2 = full_table[full_table['REGIÓN'] == region]
                options_region, options_provincia = create_dropdown_options(full_table2)
                full_table2 = full_table2[full_table2['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table2.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table2.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            dropdown_region = dcc.Dropdown(
                options = options_region,
                value = region,
                placeholder ='Región',
                id = 'region',
                disabled=False
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (provincia is not None) and (provincia != '') and (n_clicks + n_submit == 0):
            full_table3 = full_table[full_table['REGIÓN'] == region]
            full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table4.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            options_region, options_provincia = create_dropdown_options(full_table3)
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value = provincia,
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (provincia is not None) and (provincia != '') and (input_value != '') and (n_clicks + n_submit > 0):  
            try:
                is_int = int(input_value)  
                full_table3 = full_table[full_table['REGIÓN'] == region]
                full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
                options_region, options_provincia = create_dropdown_options(full_table3)
                full_table4['RUC_ENTIDAD'] = full_table4['RUC_ENTIDAD'].astype(str)
                full_table4 = full_table4[full_table4['RUC_ENTIDAD'].str.contains(input_value)]
            except:
                input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                input_value = normalize('NFC', input_value)
                input_value = input_value.upper()
                full_table3 = full_table[full_table['REGIÓN'] == region]
                full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
                options_region, options_provincia = create_dropdown_options(full_table3)
                full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                    row_selectable='single',
                    selected_rows=[],
                    data = full_table4.to_dict('records'),
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                )
            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value = provincia,
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia], [dropdown_region], 0

        elif (region is not None) and (region  != '') and (input_value != '') and (n_clicks + n_submit > 0):   
            if  (provincia is not None) and (provincia != ''):
                try:
                    is_int = int(input_value)
                    full_table3 = full_table[full_table['REGIÓN'] == region]
                    full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
                    options_region, options_provincia = create_dropdown_options(full_table3)
                    full_table4['RUC_ENTIDAD'] = full_table4['RUC_ENTIDAD'].astype(str)
                    full_table4 = full_table4[full_table4['RUC_ENTIDAD'].str.contains(input_value)]
                except:

                    input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                    input_value = normalize('NFC', input_value)
                    input_value = input_value.upper()
                    full_table3 = full_table[full_table['REGIÓN'] == region]
                    full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
                    options_region, options_provincia = create_dropdown_options(full_table3)
                    full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value ='',
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
            elif (provincia is not None) and (provincia == ''):
                try:
                    is_int = int(input_value)
                    full_table3 = full_table[full_table['REGIÓN'] == region]
                    options_region, options_provincia = create_dropdown_options(full_table3)
                    full_table3['RUC_ENTIDAD'] = full_table3['RUC_ENTIDAD'].astype(str)
                    full_table4 = full_table3[full_table3['RUC_ENTIDAD'].str.contains(input_value)]
                except:
                    input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                    input_value = normalize('NFC', input_value)
                    input_value = input_value.upper()
                    full_table3 = full_table[full_table['REGIÓN'] == region]
                    options_region, options_provincia = create_dropdown_options(full_table3)
                    full_table4 = full_table3[full_table3['ENTIDAD'].str.contains(input_value)]
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value ='',
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
        elif (region is not None) and (region  != '') and (input_value == '') and (n_clicks + n_submit > 0):
            if  (provincia is not None) and (provincia != ''):
                full_table3 = full_table[full_table['REGIÓN'] == region]
                full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
                options_region, options_provincia = create_dropdown_options(full_table3)
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value = provincia,
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
            elif (provincia is not None) and (provincia == ''):

                full_table3 = full_table[full_table['REGIÓN'] == region]
                options_region, options_provincia = create_dropdown_options(full_table3)
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value ='',
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
        if (provincia is None):
            if (input_value == '') and (n_clicks + n_submit >= 0):
                full_table4 = full_table[full_table['REGIÓN'] == region]
                options_region, options_provincia = create_dropdown_options(full_table4)
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )
                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value = provincia,
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
            if (input_value != '') and (n_clicks + n_submit > 0):
                try:
                    is_int = int(input_value) ## Se puede convertir el str buscado en número?
                    full_table4 = full_table[full_table['REGIÓN'] == region]
                    options_region, options_provincia = create_dropdown_options(full_table4)
                    full_table4['RUC_ENTIDAD'] = full_table4['RUC_ENTIDAD'].astype(str)
                    full_table4 = full_table4[full_table4['RUC_ENTIDAD'].str.contains(input_value)]
                except:
                    input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
                    input_value = normalize('NFC', input_value)
                    input_value = input_value.upper()
                    full_table4 = full_table[full_table['REGIÓN'] == region]
                    options_region, options_provincia = create_dropdown_options(full_table4)
                    full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
                table = dash_table.DataTable(
                        id = 'Entities',
                        columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table4.columns
                            ],
                        row_selectable='single',
                        selected_rows=[],
                        data = full_table4.to_dict('records'),
                        style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                    )
                dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value = region,
                    placeholder ='Región',
                    id = 'region',
                    disabled=False
                    )

                dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value ='',
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=False
                    )
                return [table], [dropdown_provincia], [dropdown_region], 0
    else:
        if reset == 0:
            full_table = full_table.iloc[selected_rows]
            options_region, options_provincia = create_dropdown_options(full_table)
            table = dash_table.DataTable(
                    id = 'Entities',
                    columns=[
                        {"name": i, "id": i} for i in full_table.columns
                    ],
                    data = full_table.to_dict('records'),
                    selected_rows=selected_rows,
                    style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'} 
                )

            dropdown_region = dcc.Dropdown(
                    options = options_region,
                    value ='',
                    placeholder ='Región',
                    id = 'region',
                    disabled=True
                    )

            dropdown_provincia = dcc.Dropdown(
                    options = options_provincia,
                    value ='',
                    placeholder ='Provincia',
                    id = 'provincia',
                    disabled=True
                    )
            
            RUC = full_table['RUC_ENTIDAD'].max()
            
            corrupcion, ejecucion, estado, contrataciones = get_data_dash(db, db2, RUC)
            
            gauge_corrupcion = [
                daq.Gauge(
                                id='corrupcion',
                                label="Nivel de Corrupción",
                                value = corrupcion,
                                max=db['CORRUPCIÓN'].max(),
                                min = 0,
                                color='#6d7e7d'
                            )
            ]

            gauge_avance = [
                daq.Gauge(
                                id='avance',
                                label="Ejecución del Gasto",
                                value = ejecucion,
                                max=100,
                                min = 0,
                                color='#6d7e7d'
                            )
            ]
            
            bar = go.Figure([
                                    go.Bar(x=estado['Type'], y=estado['Value'], marker_color='#6d7e7d')
                            ],
                            layout=go.Layout(
                                title={'text': '<b>Estado de las Contrataciones (%% del total)', 'xanchor': 'center', 'yanchor': 'top', 'x': 0.5},
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(
                                    color='black',
                                    size=10),
                                legend={'font': {'color': 'black'}},
                                font_color='black'
                            ))
            
            table_contratos = dash_table.DataTable(
                id='Contratos',
                columns=[
                    {'name':i, 'id':i} for i in contrataciones.columns
                ],
                data = contrataciones.to_dict('records'),
                style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
            )

            col = dbc.Col([
                dbc.Row([table]),
                dbc.Row([
                    html.Div([
                        html.Br(),
                        html.Div([
                            dbc.Row([
                                dbc.Col(gauge_corrupcion),
                                dbc.Col(gauge_avance)                                
                            ]),
                            dbc.Row([dbc.Col(dcc.Graph(id='estado', figure=bar, className='bar'))]),
                            dbc.Row(html.H2('Historial de Contrataciones', className='historial')),
                            dbc.Row([table_contratos]),
                            dbc.Row(html.Div([
                                html.Br()
                            ]))
                        ])
                        ]
                        )                    
                ])
            ])

            return [col], [dropdown_provincia], [dropdown_region], 0
        else:
            print(full_table)
            table = dash_table.DataTable(
                            id = 'Entities',
                            columns=[
                                {"name": i, "id": i, "selectable": True} for i in full_table.columns
                            ],
                            row_selectable='single',
                            selected_rows=[],
                            data = full_table.to_dict('records'),
                            style_header={
                                'background-color':'#6d7e7d',
                                'color': '#ffffff',
                                'text-align': 'left',
                                'font-weight': 'bold',
                                'padding': '12px 15px'
                            },
                            style_cell={
                                'textAlign':'left', 
                                'border-left':'0px',
                                'border-right':'0px',
                            },
                            style_table={
                                'border-bottom':'1px solid #dddddd',
                                'border-radius':'15px 15px 0 0',
                                'overflow':'hidden',
                                'box-shadow':'0 0 20px rgba(0,0,0,0.15)'}
                            
                        )
            dropdown_region = dcc.Dropdown(
                options = options_region,
                value = region,
                placeholder ='Región',
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

            return [table], [dropdown_provincia], [dropdown_region], 0



    

