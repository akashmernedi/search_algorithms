import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
class Stack():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0
    
    def states(self, state):
        for node in self.frontier:
            if node.state == state:
                return True
        return False

    # Removes last element from frontier LIFO
    def remove(self):
        if self.empty():
            raise Exception("The Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
class Queue(Stack):
    
    # Removes the first element from frontier FIFO
    def remove(self):
        if self.empty():
            raise Exception("The Frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Maze():
    def __init__(self, filename):
        
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # calculating the dimensions of the maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # reading the walls in the maze
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def bfs(self):

        # calculating the states explored
        self.states_explored = 0

        # Initialize the frontier to the start
        start = Node(state=self.start, parent=None, action=None)
        frontier = Stack()
        frontier.add(start)

        # Tracks the explored states
        self.explored = set()

        while True:
            
            if frontier.empty():
                raise Exception("There is no solution")

            # Select a node from the frontier
            node = frontier.remove()
            self.states_explored += 1

            # If selected node is goal then it is solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Marking the nodes as explored
            self.explored.add(node.state)

            # Adding the neighboring nodes to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.states(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    
    def dfs(self):

        # calculating the states explored
        self.states_explored = 0

        # Initialize the frontier to the start
        start = Node(state=self.start, parent=None, action=None)
        frontier = Queue()
        frontier.add(start)

        # Tracks the explored states
        self.explored = set()

        while True:
            
            if frontier.empty():
                raise Exception("There is no solution")

            # Select a node from the frontier
            node = frontier.remove()
            self.states_explored += 1

            # If selected node is goal then it is solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Marking the nodes as explored
            self.explored.add(node.state)

            # Adding the neighboring nodes to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.states(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


def main():
    maze = Maze(sys.argv[1])
    print("Maze:")
    maze.print()
    choice =  input("Enter BFS/DFS to solve the above maze: ").upper()
    if choice == 'BFS':
        maze.bfs()
        maze.print()
    elif choice == 'DFS':
        maze.dfs()
        maze.print()
    else:
        print("Invalid input!")


if __name__ == "__main__":
    main()