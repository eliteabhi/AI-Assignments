from graph import *

# ----------------------------------------------------------------

# Setup Virus

class Virus():
    def __init__( self, name: str, starting_city: str ) -> None:
        self.name: str = name
        self.starting_city: str = starting_city
        self.infected_cities: list = []

    def __str__( self ) -> str:
        return f'Virus Name: { self.name }, Starting City: { self.starting_city }, Visited Cities: { self.infected_cities }'

    def __repr__( self ) -> str:
        return f'{ self.__str__() }\n\n'

# ----------------------------------------------------------------

# Draw route on plot

def draw_route( city_from: str, city_to: str, cities_graph: Graph ) -> None:
    city_f: City = cities_graph.get_node_by_name( city_from ).city
    city_t: City = cities_graph.get_node_by_name( city_to ).city
    
    lats: list = [ city_f.get_coords()[ 1 ], city_t.get_coords()[ 1 ]  ]
    lons: list = [ city_f.get_coords()[ 0 ], city_t.get_coords()[ 0 ]  ]
    plt.plot( lats, lons, 'red', lw=1 )

# ----------------------------------------------------------------

# Uninformed Search to spread to all cities

def uninformed_bfs( virus: Virus, cities_graph: Graph ) -> None:
    queue: list = [ virus.starting_city ]

    last_city_queue: list = []
    last_city: str = virus.starting_city

    distance: float = 0.0

    nodes_till_next_layer: int = 0
    layer_nodes_queue: list = []

    while queue:
        current_city: str = queue.pop( 0 )

        if current_city not in virus.infected_cities:
            print( f'Virus `{ virus.name }` spreading to { current_city }' )
            virus.infected_cities.append( current_city )

            available_routes = cities_graph.get_node_by_name( current_city ).get_routes()

            if last_city != current_city:
                distance += available_routes.get( last_city )
                draw_route( last_city,  current_city, cities_graph )
                plt.show()

            for key in virus.infected_cities:
                available_routes.pop( key, None )

            for key in queue:
                available_routes.pop( key, None )

            if len( available_routes ) > 0:
                layer_nodes_queue.append( len( available_routes ) )
                last_city_queue.append( current_city )

            if nodes_till_next_layer == 0 and last_city_queue:
                last_city = last_city_queue.pop( 0 )
                nodes_till_next_layer = layer_nodes_queue.pop( 0 )

            nodes_till_next_layer -= 1
            queue.extend( available_routes.keys() )

    print( f'\nVirus `{ virus.name }` started in `{ virus1.starting_city }` and ended in `{ last_city }`, with a total distance of `{ distance }` miles, infecting `{ len( virus.infected_cities ) }` cities')

# ----------------------------------------------------------------

# Run the simulation

virus1: Virus = Virus( name='Ligma', starting_city='Three Rivers' )
print()
setup_plot()
uninformed_bfs( virus1, city_graph, delay=10 )
print()

# ----------------------------------------------------------------

import heapq

# ----------------------------------------------------------------

# Informed search

def informed_Astar(starting_city: str, ending_city: str, cities_graph: Graph ) -> None:
    queue: list = [ ( 0, starting_city, [ starting_city ] ) ]
    cost_so_far: dict = { starting_city: 0 }

    while queue:
        _, current_city, path = heapq.heappop( queue )
        print( f'At { current_city }' )

        if current_city == ending_city:
            break

        for neighbor, distance in cities_graph.get_node_by_name( current_city ).get_routes().items():
            tentative_cost = cost_so_far[ current_city ] + distance

            if neighbor not in cost_so_far or tentative_cost < cost_so_far[ neighbor ]:
                cost_so_far[ neighbor ] = tentative_cost
                priority = tentative_cost + cities_graph.get_heuristic( cities_graph.get_node_by_name( neighbor ), cities_graph.get_node_by_name( ending_city ) )
                heapq.heappush( queue, ( priority, neighbor, path + [neighbor] ) )

    print( f'\nThe shortest path from { starting_city } to { ending_city } is { cost_so_far[ ending_city ] } miles long' )
    print( f'The route to take is { path }' )

informed_Astar( starting_city='San Antonio', ending_city='College Station', cities_graph=city_graph )

