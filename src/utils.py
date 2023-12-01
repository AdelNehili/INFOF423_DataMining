from glob import glob
from os.path import join, dirname, basename
from os import listdir
import pandas as pd
import numpy as np
from io import StringIO
import json

COLS = [
    "mapped_veh_id",
    "RS_E_OilPress_PC2",
    "RS_E_OilPress_PC1",
    "RS_E_RPM_PC1",
    "RS_E_RPM_PC2",
    "RS_E_InAirTemp_PC1",
    "RS_E_InAirTemp_PC2",
    "RS_E_WatTemp_PC1",
    "RS_E_WatTemp_PC2",
    "RS_T_OilTemp_PC1",
    "RS_T_OilTemp_PC2"
]

COL_TYPES = {"mapped_veh_id": np.int32,
            #"RS_E_OilPress_PC1": np.int32,
            #"RS_E_OilPress_PC2": np.int32,
            #"RS_E_RPM_PC1": np.int32,
            #"RS_E_RPM_PC2": np.int32,
            #"RS_E_InAirTemp_PC1": np.int32,
            #"RS_E_InAirTemp_PC2": np.int32,
            #"RS_E_WatTemp_PC1": np.int32,
            #"RS_E_WatTemp_PC2": np.int32,
            #"RS_T_OilTemp_PC1": np.int32,
            #"RS_T_OilTemp_PC2": np.int32
            }

def get_data_files(dir=join(dirname(dirname(__file__)), "data")):
    return [{"value": f, "label": basename(f)} for f in glob(join(dir, "*.csv"))]


def load_df(file):
    if not file:
        return
    return pd.read_csv(file, delimiter=";", index_col=0, dtype=COL_TYPES)

def get_columns(df):
    if df is None:
        return []
    return list(df)

def get_vehicule_ids(df):
    if df is None:
        return []
    return [str(e) for e in sorted(df["mapped_veh_id"].unique())]

def df_to_dict(df):
    if df is None:
        return
    return df.to_dict("records")

def df_to_json(df):
    if df is None:
        return
    return df.to_json(date_format='iso', orient='split')

def json_to_df(data):
    if not data:
        return
    return pd.read_json(StringIO(data), orient='split')

def filter_df(df, filters):
    if df is None:
        return
    filtered_df = df
    if "vehicules" in filters and filters["vehicules"]:
        filtered_df = filtered_df[filtered_df['mapped_veh_id'].isin(list(map(int, filters["vehicules"])))]
    if "features" in filters and filters["features"]:
        filtered_df = filtered_df[filters["features"]]
    
    return filtered_df