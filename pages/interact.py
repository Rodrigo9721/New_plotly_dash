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
from data import data, create_dropdown_options
import re
from unicodedata import normalize
import platform

def update_output_search(provincia, region, input_value, n_clicks, n_submit, reset):
    db = pd.read_csv('unica.csv', encoding='latin-1')
    db2 = pd.read_csv('anualizada.csv', encoding='latin-1')
    db, db2 = data(db, db2)
    options_provincia = create_dropdown_options(db)[1]
    full_table = db[['ENTIDAD', 'REGIÓN', 'PROVINCIA', 'RUC_ENTIDAD']].sort_values(by=['REGIÓN'], ascending=True)
    if region is None:
        if (input_value == '') and (n_clicks + n_submit == 0):
            table = dash_table.DataTable(
                        id = 'Entities',
                        data = full_table.to_dict('records'),
                        style_cell=dict(textAlign='left'),
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=True
                )
            return [table], [dropdown_provincia]
        elif (input_value == '') and (n_clicks + n_submit > 0):
            
            table = dash_table.DataTable(
                        id = 'Entities',
                        data = full_table.to_dict('records'),
                        style_cell=dict(textAlign='left'),
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=True
                )
            return [table], [dropdown_provincia]
        elif (input_value != '') and (n_clicks + n_submit > 0):
            input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
            input_value = normalize('NFC', input_value)
            input_value = input_value.upper()
            full_table = full_table[full_table['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                        id = 'Entities',
                        data = full_table.to_dict('records'),
                        style_cell=dict(textAlign='left'),
                    )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=True
                )
            return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  == '') and (n_clicks + n_submit == 0):
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=True
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  == '') and (input_value == '') and (n_clicks + n_submit > 0):
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=True
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  == '') and (input_value != '') and (n_clicks + n_submit > 0):
        input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
        input_value = normalize('NFC', input_value)
        input_value = input_value.upper()
        full_table = full_table[full_table['ENTIDAD'].str.contains(input_value)]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=True
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (n_clicks + n_submit == 0):
        full_table2 = full_table[full_table['REGIÓN'] == region]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table2.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table2)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=False
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (input_value == '') and (n_clicks + n_submit > 0):
        full_table2 = full_table[full_table['REGIÓN'] == region]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table2.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table2)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=False
            )
        return [table], [dropdown_provincia]

    elif (region is not None) and (region  != '') and (provincia is not None) and (provincia == '') and (input_value != '') and (n_clicks + n_submit > 0):
        input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
        input_value = normalize('NFC', input_value)
        input_value = input_value.upper()
        full_table2 = full_table[full_table['REGIÓN'] == region]
        options_provincia = create_dropdown_options(full_table2)[1]
        full_table2 = full_table2[full_table2['ENTIDAD'].str.contains(input_value)]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table2.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value ='',
            placeholder ='Provincia',
            id = 'provincia',
            disabled=False
            )
        return [table], [dropdown_provincia]

    elif (region is not None) and (region  != '') and (provincia is not None) and (provincia != '') and (n_clicks + n_submit == 0):
        full_table3 = full_table[full_table['REGIÓN'] == region]
        full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table4.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        options_provincia = create_dropdown_options(full_table3)[1]
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value = provincia,
            placeholder ='Provincia',
            id = 'provincia',
            disabled=False
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  != '') and (provincia is not None) and (provincia != '') and (input_value != '') and (n_clicks + n_submit > 0):      
        input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
        input_value = normalize('NFC', input_value)
        input_value = input_value.upper()
        full_table3 = full_table[full_table['REGIÓN'] == region]
        full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
        options_provincia = create_dropdown_options(full_table3)[1]
        full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
        table = dash_table.DataTable(
                id = 'Entities',
                data = full_table4.to_dict('records'),
                style_cell=dict(textAlign='left'),
            )
        dropdown_provincia = dcc.Dropdown(
            options = options_provincia,
            value = provincia,
            placeholder ='Provincia',
            id = 'provincia',
            disabled=False
            )
        return [table], [dropdown_provincia]
    
    elif (region is not None) and (region  != '') and (input_value != '') and (n_clicks + n_submit > 0):   
        if  (provincia is not None) and (provincia != ''):
            input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
            input_value = normalize('NFC', input_value)
            input_value = input_value.upper()
            full_table3 = full_table[full_table['REGIÓN'] == region]
            full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
            options_provincia = create_dropdown_options(full_table3)[1]
            full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]
        elif (provincia is not None) and (provincia == ''):
            input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
            input_value = normalize('NFC', input_value)
            input_value = input_value.upper()
            full_table3 = full_table[full_table['REGIÓN'] == region]
            options_provincia = create_dropdown_options(full_table3)[1]
            full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]
    elif (region is not None) and (region  != '') and (input_value == '') and (n_clicks + n_submit > 0):
        if  (provincia is not None) and (provincia != ''):
            full_table3 = full_table[full_table['REGIÓN'] == region]
            full_table4 = full_table3[full_table3['PROVINCIA'] == provincia]
            options_provincia = create_dropdown_options(full_table3)[1]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value = provincia,
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]
        elif (provincia is not None) and (provincia == ''):
            
            full_table3 = full_table[full_table['REGIÓN'] == region]
            options_provincia = create_dropdown_options(full_table3)[1]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]
    if (provincia is None):
        if (input_value == '') and (n_clicks + n_submit >= 0):
            full_table4 = full_table[full_table['REGIÓN'] == region]
            options_provincia = create_dropdown_options(full_table4)[1]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )
            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value = provincia,
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]
        if (input_value != '') and (n_clicks + n_submit > 0):
            input_value = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", input_value), 0, re.I)
            input_value = normalize('NFC', input_value)
            input_value = input_value.upper()
            full_table4 = full_table[full_table['REGIÓN'] == region]
            options_provincia = create_dropdown_options(full_table4)[1]
            full_table4 = full_table4[full_table4['ENTIDAD'].str.contains(input_value)]
            table = dash_table.DataTable(
                    id = 'Entities',
                    data = full_table4.to_dict('records'),
                    style_cell=dict(textAlign='left'),
                )

            dropdown_provincia = dcc.Dropdown(
                options = options_provincia,
                value ='',
                placeholder ='Provincia',
                id = 'provincia',
                disabled=False
                )
            return [table], [dropdown_provincia]


