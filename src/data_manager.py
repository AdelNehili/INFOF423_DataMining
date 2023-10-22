import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#____Filtering Chunks
def filter_chunk(chunk, filters, debug=False):
    """
    Filters a chunk based on provided conditions.
    It allows to add as much conditions as wanted. 
    After filtering data, it modify the 'timestamps_UTC' to fit
     
    Args:
    - chunk (pd.DataFrame): The chunk of data to filter.
    - **conditions (dict): Conditions to apply on the chunk. 
                           Key is column name and value is the condition for that column.

    Returns:
    - pd.DataFrame: Filtered chunk
    """
    for column, (min_val, max_val) in filters.items():
        #chunk = chunk[(chunk[column] >= min_val) & (chunk[column] <= max_val)]
        #chunk[column] = pd.to_numeric(chunk[column], errors='coerce')
        chunk = chunk[(chunk[column] >= min_val) & (chunk[column] <= max_val)]

    if debug:
        display_terminal_chunk_data(chunk)
    
    if 'timestamps_UTC' in chunk.columns:
        convert_dateString_to_timestamps(chunk)

    
    return chunk
def convert_dateString_to_timestamps(chunk):

    """
        This function modify the 'timestamps_UTC' String type to DateTime. It allows to display graph with notion of time.
        It should also allows to apply some mathematic tools as gradiant.

        Since we want to modify the whole dataFrame (for previous reasons), let's directly modify it via ".loc[:,'timestamps_UTC']"
    """
    if 'timestamps_UTC' in chunk.columns:
        # Convert the 'timestamps_UTC' column to datetime format
        chunk.loc[:,'timestamps_UTC'] = pd.to_datetime(chunk['timestamps_UTC'])

        # Convert datetime to timestamp
        chunk.loc[:,'timestamps_UTC'] = chunk['timestamps_UTC'].apply(lambda x: x.timestamp())


#____Terminal Display
def display_column_name(chunks):
    # Get the first chunk
    first_chunk = next(chunks)

    for col_name in first_chunk.columns:
            print(f"{col_name}", end=",")
def display_all_data(chunks):
    #Allows to display the data chunk by chunk
    for chunk_id, chunk in enumerate(chunks):
        if chunk_id == 1:
            print(f"Here's the chunk {chunk_id}")
            print(tabulate(chunk, headers='keys', tablefmt='grid'))
            print("-"*50+"\n"*2)
def display_terminal_chunk_data(chunk):

    # Display the selected columns from the first chunk
    print(tabulate(chunk, headers='keys', tablefmt='grid'))


#____Graph Display
def display_2D_graph(current_chunk,xLabel, yLabel, linked_graph = False):

    plt.figure()
    if linked_graph:
        plt.plot(current_chunk[xLabel], current_chunk[yLabel], 'o-', color='blue')
    else:
        plt.plot(current_chunk[xLabel], current_chunk[yLabel], 'o', color='blue')
    
    
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(f"{xLabel} Vs {yLabel}")
    plt.grid()
    plt.show()

def display_3D_graph(data,xLabel,yLabel,zLabel):

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(data[xLabel], data[yLabel], data[zLabel], c='blue', marker='o')
         
    ax.set_xlabel(f"{xLabel}")
    ax.set_ylabel(f"{yLabel}")
    ax.set_zlabel(f"{zLabel}")
    ax.set_title(f'3D plot of {xLabel}, {yLabel}, and {zLabel}')

    plt.show()
def display_3D_graph_linked(data,xLabel,yLabel,zLabel):


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(data[xLabel], data[yLabel], data[zLabel], c='blue', marker='o')
    
    # Line plot to link the points
    ax.plot(data[xLabel], data[yLabel], data[zLabel], color='blue')

    ax.set_xlabel(f"{xLabel}")
    ax.set_ylabel(f"{yLabel}")
    ax.set_zlabel(f"{zLabel}")
    ax.set_title(f'3D plot of {xLabel}, {yLabel}, and {zLabel}')

    plt.show()




