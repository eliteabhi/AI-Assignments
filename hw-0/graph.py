# Add only your imports here
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import time
from PIL import Image
from math import ceil
from typing import Any, Tuple, Union

# ----------------------------------------------------------------

# Assume that the data files are in the following folder -- THIS WILL BE USED BY THE TA

basePath = r"/content/drive/My Drive/Colab Notebooks/Artificial Intelligence/Data"
basePath = r"."

TEXAS_MAP: str = rf'{basePath}/cities-texas-map.png'

map_grid = ( 22 * 10, 9 * 10 )

# ----------------------------------------------------------------

# Load Data

def load_csvs() -> Tuple[ pd.DataFrame, pd.DataFrame ]:
    city_coords: pd.DataFrame = pd.read_csv( fr'{ basePath }/city-texas.csv', names=[ 'City', 'Longitude', 'Latitude' ] )
    city_distances: pd.DataFrame = pd.read_csv( fr'{ basePath }/city-distance-texas.csv', names=[ 'City_From', 'City_To', 'Distance' ] )

    print( city_coords )
    print()
    print( city_distances )
    print()

    return city_coords, city_distances

# ----------------------------------------------------------------

# Setup Graph and Nodes

class City():

    def __init__( self, name: str, longitude: float, latitude: float ) -> None:
        self.name: str = name
        self.longitude: float = longitude
        self.latitude: float = latitude

    def __str__( self ) -> str:
        return f'Name: { self.name }, Longitude: { self.longitude }, Latitude: { self.latitude }'

    def __repr__( self ) -> str:
        return f'{ self.__str__() }\n\n'

    def get_coords( self ) -> Tuple[ float, float ]:
        return self.longitude, self.latitude

class Node():
    def __init__( self, city: City = None, routes: dict = None ) -> None:
        self.city: City = city
        self.routes: dict = routes

    def __str__( self ) -> str:
        return f'City:\n    { self.city }\nRoutes:\n   { self.routes }'

    def __repr__( self ) -> str:
        return f'{ self.__str__() }\n\n'

    def set_routes( self, routes: dict ) -> None:
        self.routes = routes

    def get_routes( self ) -> Union[ dict | None ]:
        return self.routes

class Graph():

    def __init__( self, graph: list ) -> None:
        self.graph: list = graph

    def __str__( self ) -> str:
        return f'{ self.graph }'

    def insert( self, node: Node ) -> None:
        self.graph.append( node )

    def get_node_by_name( self, name ) -> Union[ Node, None ]:
        return next( ( node for node in self.graph if node.city.name == name ), None )

    def get_heuristic( self, node1: Node, node2: Node ) -> float:
        return abs( node1.city.longitude - node2.city.longitude ) + abs( node1.city.latitude - node2.city.latitude )

# ----------------------------------------------------------------

# Populate Graph

cities, city_routes = load_csvs()

city_graph: Graph = Graph( [] )

for i, rows in cities.iterrows():
    temp: Node = Node()
    temp.city = City( name=rows[ 'City' ], longitude=rows[ 'Longitude' ], latitude=rows[ 'Latitude' ] )

    routes: dict = {}
    routes |= (
        city_routes.loc[ city_routes[ 'City_From' ] == temp.city.name ]
        .drop( columns=[ 'City_From' ] )
        .to_dict( orient='tight' )
        .get( 'data' )
    )
    routes.update( city_routes.loc[ city_routes[ 'City_To' ] == temp.city.name ].drop( columns=[ 'City_To' ] ).to_dict( orient='tight' ).get( 'data' ) )
    temp.routes = routes

    city_graph.insert( temp )

print( city_graph )

# ----------------------------------------------------------------

# Setup Grid on Image

def setup_plot() -> None:
    # Visualize Graph
    G = nx.Graph()

    for index, row in city_routes.iterrows():
        G.add_edge( row[ 'City_From' ], row[ 'City_To' ], weight=row[ 'Distance' ] )

    pos = nx.spring_layout(G)
# nx.draw( G, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=5, font_color='black' )

    image = mpimg.imread( TEXAS_MAP )

    # Set up the plot
    _, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(image, extent=[-107, -93, 25, 37])
    
    for _, row in cities.iterrows():
        city = row['City']
        lat = row['Longitude']
        lon = row['Latitude']
        ax.plot(lon, lat, 'bo', markersize=5)  # Plot city as blue circles ('bo')
        ax.text(lon + 0.1, lat, city, fontsize=9, color='black')  # Add city names slightly offset
