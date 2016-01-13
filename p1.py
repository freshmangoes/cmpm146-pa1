# Kyle Cilia
# Dijkstra's in a Dungeon
# PA1
# CMPM146

from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    dist = {}  # distance from source to destination
    prev = {}  # previous node in optimal path from source
    queue = []  # queue initialization
    dist[initial_position] = 0
    prev[initial_position] = None #prev from source
    #queue = [0, start]
    heappush(queue, (dist[initial_position], initial_position))

    while queue:
        # Pop least cost node
        curr_cost, curr_node = heappop(queue)
        # Debug statements
        # print("curr_node: " + str(curr_node)+ "\n")
        # print("curr_cost: " + str(curr_cost)+ "\n")\
        # Once we find the destination, break the loop
        if curr_node == destination:
            break
        # Use navigation_edges to get adjacent cells
        adjacent = adj(graph, curr_node)
        # Iterate through adjacency list and calculate cost
        for acell, cost in adjacent:
            # Variable to store cost of path consisting of current cost and the cost of the
            # adjacent cell
            pathcost = curr_cost + cost
            if acell not in dist or pathcost < dist[acell]:
                dist[acell] = pathcost
                prev[acell] = curr_node
                heappush(queue, (pathcost, acell))
    # Build path to return

    if curr_node == destination:
        path = []
        # Building path in reverse order because we're at the destination
        while curr_node:
            path.append(curr_node)
            curr_node = prev[curr_node]
        # Reversing the path
        path.reverse()
        return path
    else:
        # Return empty list if there is no path
        return []
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    dist = {}  # distance from source to destination
    prev = {}  # previous node in optimal path from source
    queue = []  # queue initialization
    dist[initial_position] = 0
    prev[initial_position] = None #prev from source


    heappush(queue, (dist[initial_position], initial_position))

    while queue:
        curr_cost, curr_node = heappop(queue)
        # Use navigation_edges to get adjacent cells
        adjacent = adj(graph, curr_node)
        # Iterate through adjacency list and calculate cost
        for acell, cost in adjacent:
            # Variable to store cost of path consisting of current cost and the cost of the
            # adjacent cell
            tempcost = curr_cost + cost

            # if acell not in queue or tempcost < dist[acell]:
            dist[acell] = tempcost
            prev[acell] = curr_node
        print(dist)
    return dist

    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    # List to return
    adjacency_list = []
    # deltas for x coordinate
    for dx in (-1, 0, 1):
        # deltas for y coordinates
        for dy in (-1, 0, 1):
            # get adjacent cell using deltas
            adjcell = (cell[0] + dx, cell[1] + dy)
            # if statement for normal cost formula, checking if the cell is not in a corner
            if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
                # checking to make sure adjcell is a space rather than a wall
                if adjcell in level['spaces']:
                    adjacent = (adjcell, level['spaces'][adjcell]/2 + level['spaces'][cell]/2)
                    # print("Normal adj: " + str(adjacent) + "\n")
                    adjacency_list.append(adjacent)
            # if statement for diagonal cost formula, checking if cell is a corner
            if (dx != 0 and dy != 0):
                if adjcell in level['spaces']:
                    adjacent = (adjcell, (sqrt(2)*0.5*level['spaces'][adjcell]) + (sqrt(2)*0.5*level['spaces'][cell]))
                    # print("Diagonal adj: " + str(adjacent) + "\n")
                    adjacency_list.append(adjacent)
            # Do nothing if both change in x and y is not 0 because that is the origin cell
    # print("Adjacency list:")
    # print(adjacency_list)
    return adjacency_list
    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'


    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')

