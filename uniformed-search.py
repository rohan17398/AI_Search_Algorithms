import collections
import copy
import heapq
import random


class Node:
  def __init__(self, state, action, cost, parent):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent


def get_action_history(node):
  history = []
  while node.parent:
    history.append(node.action)
    node = node.parent
  history.reverse()
  return history


class Environment:
  def __init__(self):
    self.nodes_expanded = 0

  def is_goal(self, node):
    self.nodes_expanded += 1
    return self.goal_test(node.state)

  def get_successors(self, node):
    state = node.state
    return [
      Node(self.successor(state, action), action, cost, node)
      for (action, cost) in self.get_actions(state)
    ]


class VacuumEnvironment(Environment):
  def init_state(self):
    return {"agent_loc": 0, "tiles": ["dirty"] * 5}

  def goal_test(self, state):
    for tile in state["tiles"]:
      if tile != "clean":
        return False
    return True

  def get_actions(self, state):
    return [("left", 1), ("right", 1), ("suck", 1)]

  def successor(self, state, action):
    next_state = copy.deepcopy(state)
    agent_loc = state["agent_loc"]
    if agent_loc < len(state["tiles"]) - 1 and action == "right":
      next_state["agent_loc"] += 1
    elif agent_loc > 0 and action == "left":
      next_state["agent_loc"] -= 1
    elif state["tiles"][agent_loc] == "dirty" and action == "suck":
      next_state["tiles"][agent_loc] = "clean"
    return next_state


class SmallRomanianPathfindingEnvironment(Environment):
  def init_state(self):
    return "Sibiu"

  def goal_test(self, state):
    return state == "Bucharest"

  def get_actions(self, state):
    if state == "Sibiu":
      return [("Fagaras", 99), ("Rimnicu Vilcea", 80), ("Atlantis", 1)]
    elif state == "Fagaras":
      return [("Sibiu", 99), ("Bucharest", 211)]
    elif state == "Rimnicu Vilcea":
      return [("Sibiu", 80), ("Pitesti", 97)]
    elif state == "Pitesti":
      return [("Rimnicu Vilcea", 97), ("Bucharest", 101)]
    elif state == "Bucharest":
      return [("Fagaras", 211), ("Pitesti", 101)]
    elif state == "Atlantis":
      return [("Bucharest", 10000)]
    else:
      return []

  def successor(self, state, action):
    return action


class IncrementalNQueensEnvironment(Environment):
  def locs_diagonal(_, loc1, loc2):
    row_diff = abs(loc1[0] - loc2[0])
    col_diff = abs(loc1[1] - loc2[1])
    return row_diff == col_diff

  def visualize(self, state):
    printable_state = ""
    for row in range(0, self.size):
      for col in range(0, self.size):
        printable_cell = "Q" if (row, col) in state else "."
        printable_state += printable_cell
      printable_state += "\n"
    return printable_state

  def init_state(self):
    self.size = 6
    return []

  def goal_test(self, state):
    if len(state) != self.size:
      return False
    for piece_loc in state:
      (x, y) = piece_loc
      for other_loc in state:
        if other_loc == piece_loc:
          continue
        if other_loc[0] == x or other_loc[1] == y or self.locs_diagonal(piece_loc, other_loc):
          return False
    return True

  def get_actions(self, state):
    if len(state) < self.size:
      row = len(state)
      return [((row, col), 1) for col in range (0, self.size)]
    return []

  def successor(self, state, action):
    next_state = copy.deepcopy(state)
    next_state.append(action)
    return next_state


def first_action_agent(root, env):
  node = root
  while not env.is_goal(node):
    successors = env.get_successors(node)
    node = successors[0]
  return node

def random_agent(root,env):
  node = root
  # print(len(env.state))
  # print(env.size)
  # print(env.__class__.__name__)
  # if(env.__class__.__name__ !=  "IncrementalNQueensEnvironment") :
  while not env.is_goal(node):
    successors= env.get_successors(node)
    node = random.choice(successors)
  return node
  




def dfs_agent(root,env):
  frontier=[]
  frontier.append(root)
  while frontier:
    # print(frontier)
    node=frontier.pop()
    # print(node.state)
    if env.is_goal(node):
      return node
    for successor in env.get_successors(node):
      # print(successor.state)
      frontier.append(successor)
    


def bfs_agent(root, env):
  node=root
  queue=collections.deque()
  # queue.append(root)
  queue.append(node)
  while queue:
    node = queue.popleft()
    # print(node.state)
    if env.is_goal(node):
      return node
    for x in env.get_successors(node):
      queue.append(x)


def ucs_agent(root, env):
  frontier=[]
  heapq.heappush(frontier,(0,0,root))
  # frontier.append(root)
  visited=set()
  tiebreaker=0
  while frontier:
    node=heapq.heappop(frontier)[2]
    visited.add(str(node.state))
    if env.is_goal(node):
      return node
    for successor in env.get_successors(node):
      if str(successor.state) in visited:
        continue
      tiebreaker+=1
      heapq.heappush(frontier,(successor.cost,tiebreaker,successor))

# YOUR AGENT FUNCTIONS GO HERE

def random_agent_2(root, env) :

  if env.__class__.__name__ == "IncrementalNQueensEnvironment" :
      
    node = root
    visited = set()

    i, j = -1, -1

    j = []
    times = env.size

    while times > 0 :
      successors = env.get_successors(node)

      index = 0
    
      deletable = []

      for element in successors :
        # deletable = []
        #Printing out the last element of the State
        # print('LEN', len(element.state))
        # print(element.state[-1], element.state[-1][1], j)
        if element.state[-1][1] in j :
          deletable.append(index)
          # print("Deletable 1 :", deletable)
          # deletable = index
          # deletable = element.state[-1][1]
      
        # print("Current Successor List :", str(element.state))
        index += 1
      
      # print("Deletable 2:", deletable)
      # print("Deleting all the items in the list above")

      deletable.sort(reverse=True)

    
      for position in deletable:
          del successors[position]


      for element in successors :
      
        # print("Current Successor List :", str(element.state))

        node = random.choice(successors)
        visited.add(str(node.state[-1]))
        # print("After adding in Visited")
        # print(node.state[-1])
        i = node.state[-1][0]
        j.append(node.state[-1][1])
        times -= 1
      return node 
  else :
    node = root
    while not env.is_goal(node) :
      successors = env.get_successors(node)
      node = random.choice(successors)
    return node


def main():
  env = IncrementalNQueensEnvironment() # change this line to switch environments
  root = Node(env.init_state(), None, 0, None)
  agent = ucs_agent # change this line to switch agent functions
  result = agent(root, env)
  print(get_action_history(result))
  print("Nodes expanded:", env.nodes_expanded)


if __name__ == "__main__":
  main()
