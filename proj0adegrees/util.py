class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []
        self.frontierset = set()

    def add(self, node):
        self.frontier.append(node)
        self.frontierset.add(node.state)

    def contains_state(self, state):
        return state in self.frontierset

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(-1)
            self.frontierset.remove(node.state)
            return node


class QueueFrontier(StackFrontier):

    def __init__(self):
        # I changed the queueFrontier to use a deque
        # because popping index 0 from a Python list
        # is O(n), while pop_left on a deque is O(1)
        
        from collections import deque

        self.frontier = deque()
        self.frontierset = set()

    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.popleft()
            self.frontierset.remove(node.state)
            return node
