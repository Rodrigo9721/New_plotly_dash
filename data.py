import pandas as pd
pd.options.mode.chained_assignment = None



def data(db, db2):
    db = db[['ENTIDAD', 'RANKING', 'REGIÓN', 'PROVINCIA', 'INCONDUCTA FUNCIONAL', 'CORRUPCIÓN', 'ESTADO DE CORRUPCION', 'PUNTAJE', '%DEV-2021', 'RUC_ENTIDAD']]
    return db, db2

def create_dropdown_options(tags):
    regiones = tags['REGIÓN'].unique().tolist()
    provincias = tags['PROVINCIA'].unique().tolist()
    options_R = [{'label': region, 'value': region} for region in regiones]
    options_P = [{'label': provincia, 'value': provincia} for provincia in provincias]
    return options_R, options_P

def get_data_dash(db, db2, ruc):
    corrupcion = db['CORRUPCIÓN'][db['RUC_ENTIDAD'] == ruc].max()
    ejecucion = db['DEVENGADO'][db['RUC_ENTIDAD'] == ruc].max()*100
    db3 = db2[db2['RUC_ENTIDAD'] == ruc]
    anulada = len(db3[db3['data_csv.ESTADOCONTRATACION'].str.contains('Anulada')])
    comprometida = len(db3[db3['data_csv.ESTADOCONTRATACION'].str.contains('Comprometida')])
    devengada = len(db3[db3['data_csv.ESTADOCONTRATACION'].str.contains('Devengada')])
    emitida = len(db3[db3['data_csv.ESTADOCONTRATACION'].str.contains('Emitida')])
    total = anulada + comprometida + devengada + emitida
    try:
        p_anulada = anulada/total
    except:
        p_anulada = 0
    try:
        p_comprometida = comprometida/total
    except:
        p_comprometida = 0
    try:
        p_devengada = devengada/total
    except:
        p_devengada = 0
    try:
        p_emitida = emitida/total
    except:
        p_emitida = 0
    dict_estado = {'Type':['Anulada', 'Comprometida', 'Devengada', 'Emitida'], 'Value':[p_anulada, p_comprometida, p_devengada, p_emitida]}
    estado = pd.DataFrame.from_dict(dict_estado)
    estado = estado.sort_values(by=['Value'], ascending=False)

    contrataciones = db3[['year-contrataciones', 'data_csv.TIPODECONTRATACION', 'data_csv.ESTADOCONTRATACION', 'data_csv.count', 'data_csv.median', 'data_csv.max']]
    contrataciones.rename(
        columns={'year-contrataciones':'Año', 'data_csv.TIPODECONTRATACION':'Tipo de Contratación', 'data_csv.ESTADOCONTRATACION':'Estado', 'data_csv.count':'Cantidad de Contratos', 'data_csv.median':'Monto Promedio', 'data_csv.max':'Monto Máximo'},
        inplace=True)
    contrataciones = contrataciones.sort_values(by=['Año'], ascending=True)
    return corrupcion, ejecucion, estado, contrataciones