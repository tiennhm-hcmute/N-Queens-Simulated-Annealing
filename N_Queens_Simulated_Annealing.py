# Solve N-queens problems using Simulated annealing algorithm
#https://youtu.be/7w8jk0r4lxA



from collections import deque
import numpy as np
import random
import itertools 
import math 
import tkinter as tk 
import time 

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action)
        return next_node
# ______________________________________________________________________________

class NQueensProblem:
    """The problem of placing N queens on an NxN board with none attacking each other. 
    A state is represented as an N-element array, where a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been filled in yet. We fill in columns left to right.
    
    Sample code: iterative_deepening_search(NQueensProblem(8))
    Result: <Node (0, 4, 7, 5, 2, 6, 1, 3)>
    """

    def __init__(self, N):
        #self.initial = initial 
        self.initial = tuple([-1]*no_of_queens)  # -1: no queen in that column
        self.N = N

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] is not -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            #return [(col, row) for row in range(self.N)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        """Place the next queen at the given row."""
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def value(self, node): 
        """Return (-) number of conflicting queens for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return -num_conflicts 

def schedule(t, k=20, lam=0.005, limit=10000):
    """One possible schedule function for simulated annealing"""
    #return (k * np.exp(-lam * t))
    return (k * np.exp(-lam * t) if t < limit else 0) 

def InitBoardColor():
    for r in range(no_of_queens):
        for c in range(no_of_queens):
            rect[no_of_queens*r + c].config(bg = "Orange")

def Update(state):
    for i in range(no_of_queens):
        rect[no_of_queens*i + state[i]].config(bg = "red")

def simulated_annealing(problem):
    current = Node(problem.initial)
    
    for t in itertools.count(start = 1):
        T = schedule(t)
        if T == 0:
            return current.state

        successor = current.expand(problem)
        if len(successor) == 0:
            if current.state.count(-1) > 0:
                #Lam lai
                current = Node(problem.initial)
        else:
            next = random.choice(successor)
            deltaE = problem.value(next) - problem.value(current)
            if deltaE > 0:
                current = next
            else:
                p = random.uniform(0.0, 1.0)
                if p < math.exp(deltaE/T):
                    current = next 


def MapToBoard(state):
    '''Chuyển từ state sang matrix (2D) để vẽ '''
    a = np.zeros((no_of_queens, no_of_queens), dtype = int)
    a[0::2, 1::2] = 1
    a[1::2, 0::2] = 1
    for i in range(no_of_queens):
        a[state[i], i] = -1
    return a
  
def InitBoard(state):
    board = MapToBoard(state)
    for r in range(no_of_queens):
        for c in range(no_of_queens):
            label.append(tk.Label(frame, width = 4, height = 2, bd = 0.5, relief = 'solid'))
            color = "white"
            if (r%2 == c%2):
                color = "gray"
            if board[r][c] == -1:
                color = "red"
            label[no_of_queens*r + c].config(bg = color)
            label[no_of_queens*r + c].grid(row=r, column=c)


def Solve():
    startTime = time.time()
    result = simulated_annealing(problem) 
    totalTime = time.time() - startTime
    print(result) #In result 
    InitBoard(result)
    labelTime.config(text = "Total Time: " + str(totalTime) + "sec.")
    

def SolveEvent(event):
    Solve()

if __name__ == '__main__':
    no_of_queens = 15;
    random.seed(1)

    problem = NQueensProblem(no_of_queens)

    window = tk.Tk()
    window.title("N-QUEENS")
    window.geometry("610x650+50+50")

    frame = tk.Frame(window, bd=0.5, relief="solid")
    frame.place(x = 60, y=60)

    label = []

    button = tk.Button(window, bd=0.5, relief="solid", width=8, text="SOLVE", bg = "Gray")
    button.place(x=60, y=600)
    button.bind('<Button-1>', SolveEvent)

    labelTime = tk.Label(window)
    labelTime.place(x = 150, y = 600)

    Solve()
    window.mainloop()