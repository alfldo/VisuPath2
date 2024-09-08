def bfs(maze, start, target, callback=None):
    queue = [start]
    visited = set()
    path = []
    parent = {start: None}
    
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            break
        if callback:
            callback(visited, path)
        path.append(node)
        x, y = node
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
                    parent[(nx, ny)] = node
    return path