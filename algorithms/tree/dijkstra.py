import heapq

def dijkstra(graph, start, callback=None):
    """
    Implements Dijkstra's algorithm to find the shortest path from the start node to all other nodes.

    :param graph: Dictionary where keys are node identifiers and values are dictionaries of neighbors with their weights.
    :param start: The starting node.
    :param callback: Optional function to call with updates (path and current node) during the algorithm execution.
    """
    # Priority queue to store (distance, node) tuples
    priority_queue = [(0, start)]
    
    # Distances to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Track the shortest path
    shortest_path = {}

    # Set of visited nodes
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip if node has already been visited
        if current_node in visited:
            continue
        
        visited.add(current_node)

        # Call the callback function if provided
        if callback:
            callback([], current_node)  # Pass the path and current node

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                
                # Call the callback function with updated information
                if callback:
                    path = _reconstruct_path(shortest_path, start, neighbor)
                    callback(path, neighbor)

    # Return the shortest paths
    return distances, shortest_path

def _reconstruct_path(shortest_path, start, end):
    """
    Reconstruct the shortest path from start to end using the shortest_path dictionary.

    :param shortest_path: Dictionary of nodes and their predecessors.
    :param start: The starting node.
    :param end: The ending node.
    :return: List of nodes representing the path from start to end.
    """
    path = []
    while end != start:
        path.append(end)
        end = shortest_path.get(end)
        if end is None:  # In case there is no path
            return []
    path.append(start)
    path.reverse()
    return path
