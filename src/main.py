import data_manager as dm

chunk_size = 300  # This can be adjusted based on your system's memory
chunks = dm.pd.read_csv('data/ar41_for_ulb_mini.csv', chunksize=chunk_size, delimiter=';')
all_columns = ["Unnamed: 0","mapped_veh_id","timestamps_UTC",
               "lat","lon",
               
               "RS_E_OilPress_PC1","RS_E_OilPress_PC2",

               "RS_E_RPM_PC1","RS_E_RPM_PC2",

               "RS_E_InAirTemp_PC1","RS_E_InAirTemp_PC2",
               "RS_E_WatTemp_PC1","RS_E_WatTemp_PC2",
               "RS_T_OilTemp_PC1","RS_T_OilTemp_PC2"]


# Configuration dictionary
config = {
    "columns": ["lat", "lon", "RS_E_RPM_PC1","RS_T_OilTemp_PC1", "RS_E_RPM_PC2"],
    "filters": {
        #"RS_T_OilTemp_PC1" : (75,80),
        "lat" : (0,55),
    }
}

current_chunk = next(chunks) #Select the first chunk there

aimed_data = current_chunk[config["columns"]]

filtered_chunk = dm.filter_chunk(aimed_data, config["filters"])


#dm.display_2D_graph(filtered_chunk,config["columns"][0],config["columns"][3])
#dm.display_3D_graph_linked(filtered_chunk,config["columns"][0],config["columns"][3],config["columns"][4])