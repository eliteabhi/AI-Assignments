# Add only your imports here
import pandas as pd
import numpy as np
from PIL import Image
from math import ceil
from typing import Any, Tuple, Union

# ----------------------------------------------------------------

# Assume that the data files are in the following folder -- THIS WILL BE USED BY THE TA

basePath = r"/content/drive/My Drive/Colab Notebooks/Artificial Intelligence/Data"
basePath = r"."

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

class Graph(): # TODO

    def __init__( self, graph: list ) -> None:
        self.graph: list = graph
    
    def __str__( self ) -> str:
        return f'{ self.graph }'
        
    def insert( self, node: Node ) -> None: # TODO
        self.graph.append( node )
    
# ----------------------------------------------------------------

# Populate Graph

cities, city_routes = load_csvs()

city_graph: Graph = Graph( [] )

for i, rows in cities.iterrows():
    temp: Node = Node()
    temp.city = City( name=rows[ 'City' ], longitude=rows[ 'Longitude' ], latitude=rows[ 'Latitude' ] )
    
    routes = city_routes.loc[ city_routes[ 'City_From' ] == temp.city.name ].drop( columns=[ 'City_From' ] ).to_dict( orient='tight' ).get( 'data' )
    temp.routes = dict( routes )
    
    city_graph.insert( temp )

print( city_graph )

# ----------------------------------------------------------------

# Setup Grid on Image

max_longitude = cities.loc[ cities[ 'Longitude' ].idxmax() ][ 'Longitude' ]
min_longitude = cities.loc[ cities[ 'Longitude' ].idxmin() ][ 'Longitude' ]

max_latitude = cities.loc[ cities[ 'Latitude' ].idxmax() ][ 'Latitude' ]
min_latitude = cities.loc[ cities[ 'Latitude' ].idxmin() ][ 'Latitude' ]

orig_grid_x = ceil( max( abs( min_longitude ), abs( max_longitude ) ) ) * 2
orig_grid_y = ceil( max( abs( min_latitude ), abs( max_latitude ) ) ) * 2

print( f'Longitude: { min_longitude } - { max_longitude }\n\nLatitude: { min_latitude } - { max_latitude }\n' )

def grid_from_image( path: str ) -> Tuple[ float, float ]:
    img = Image.open( path )
    width,height = img.size

    print( f'Grid: { width } x { height }\n' )
    
    return width, height

def coord_to_grid( coord: Tuple, orig_grid_size: Tuple, new_grid_size: Tuple ) -> Tuple[ int, int ]:
    new_grid_x, new_grid_y = new_grid_size
    orig_grid_x, orig_grid_y = orig_grid_size
    x, y = coord

    new_x: float = ( ( round( x ) + ( orig_grid_x / 2 ) ) / orig_grid_x ) * new_grid_x
    new_y: float = ( ( round( y ) + ( orig_grid_y / 2 ) ) / orig_grid_y ) * new_grid_y
    
    return round( new_x ), round( new_y )

map_grid = grid_from_image( fr'{ basePath }/cities-texas-map.png' )
print( f'Orig grid: { ( orig_grid_x, orig_grid_y ) }\nNew Grid: { map_grid }\n' )

for node in city_graph.graph:
    translated_coord: Tuple = coord_to_grid( node.city.get_coords(), ( orig_grid_x, orig_grid_y ), map_grid )
    
    print(f'Node City:\n { node.city }\n New Coords: { translated_coord }')
    

