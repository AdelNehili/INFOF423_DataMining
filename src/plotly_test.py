import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


import os
import glob

def delete_html_files(directory):
    """
    Deletes all HTML files in the specified directory.

    :param directory: The path to the directory containing HTML files.
    """
    # Construct the full path with pattern to match HTML files
    path_pattern = os.path.join(directory, "*.html")

    # Find all HTML files in the directory
    html_files = glob.glob(path_pattern)

    # Loop through the list of HTML files and delete each one
    for file_path in html_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
delete_html_files("doc/HTML_file")


all_columns = ["mapped_veh_id",
               "timestamps_UTC",
               "lat","lon",
               
               "RS_E_OilPress_PC1","RS_E_OilPress_PC2",

               "RS_E_RPM_PC1","RS_E_RPM_PC2",

               "RS_E_InAirTemp_PC1","RS_E_InAirTemp_PC2",
               "RS_E_WatTemp_PC1","RS_E_WatTemp_PC2",
               "RS_T_OilTemp_PC1","RS_T_OilTemp_PC2"]

col_types = {"mapped_veh_id": np.int32,
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

data = pd.read_csv("./data/cleaned_sorted_full_data.csv", delimiter=";", index_col=False)
#data = pd.read_csv("./data/ar41_for_ulb_mini.csv", delimiter=";", index_col=0, dtype=col_types)


# Focus on trains 106, 107, 131, and 196
focused_trains = [106, 107, 131, 196]
list_without_issues = [120,145,123]

for name_id in range(2,len(all_columns)):
    x_axe = "RS_E_OilPress_PC1"
    y_axe = all_columns[name_id]

    # Filter the DataFrame to include only the focused trains
    # Use the level of the MultiIndex that corresponds to 'mapped_veh_id'
    #df = data[data['mapped_veh_id'].isin(focused_trains)]
    df = data[data['mapped_veh_id'].isin(focused_trains)]

    # Plotting the Data
    # You can choose appropriate columns for x, y, size, and color based on your CSV file and analysis needs.
    fig = px.scatter(df, x=x_axe, y=y_axe,size="RS_E_RPM_PC1", color="mapped_veh_id",hover_name="RS_E_RPM_PC1", log_x=True, size_max=10)

    #fig.show()

    # Save the figure as an interactive HTML file
    fig.write_html(f"doc/HTML_file/{y_axe}_VS_{x_axe}.html")