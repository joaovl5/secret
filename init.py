from p5 import *
import networkx as nx
import random

G = nx.Graph()
f = None

NODE_DIAMETER = 50

INPUT_MULTIPLIER = 7
SCALE_MULTIPLIER = 1.1

class Node:

    # id = name of respective node in networkx graph
    # aware = level of 'awareness' of information from 0 to 1
    def __init__(self, aware, x, y):
        self.aware = aware

        self.x = x
        self.y = y 

    def draw(self, sid, font): # sid = key in dict 
       
        # node
        stroke(Color(100+(self.aware*155),100,100))
        fill(Color(50, 50 - (self.aware*50), 50  - (self.aware*50)))
        ellipse((self.x, self.y), NODE_DIAMETER, NODE_DIAMETER)
        
        # text
        fill(255)
        text_font(font, 15)
        text(str(sid), self.x, self.y - 8)

    def run(self, sid):
        # figure out neightbors 
        if self.aware > 0:



            for e in G.edges([sid]):
                print(e[0], e[1], sid)
                if(e[0] == sid or e[1] == sid):
                    weight = G.edges[e[0], e[1]]['weight']
                    neigh = nodes[e[0]] if e[0] != sid else nodes[e[1]]
                    
                    if(random.random() < weight ):
                        neigh.aware = self.aware # Binary
                    else:
                        G.edges[e[0], e[1]]['weight'] = 0

            
nodes = {}
# nodes = {
#     1: Node(1, 50, 90),
#     2: Node(0, 250, 90),
#     3: Node(0, 300, 200)
# }        

# G.add_edge(1, 2, weight=0.5)
# G.add_edge(1, 3, weight=0.5)

def node_init():
    global nodes, G

    G = nx.karate_club_graph()

    nx.draw_networkx(G)

    pos = nx.spring_layout(G, seed=3068)

    scale = 500 #scale pos 
    awares_max = 1 # number of aware nodes
    awares = 0

    for n in G.nodes():
        pos[n][0] *= scale
        pos[n][1] *= scale


        should_aware = 0
        if(awares < awares_max):
            should_aware = 1
            awares += 1
        
        nodes[n] = Node(should_aware, pos[n][0], pos[n][1])

    for u, v, w in G.edges(data=True):
        G.edges[u,v]['weight'] = round(random.random(), 3)

def setup():
    node_init()
 
    size(640, 360)

    global f

    f = create_font("fonts/arial.ttf", 16,) # Arial, 16 point, anti-aliasing on
    text_font(f, 15)
    text_align("CENTER")
    no_stroke()
    

dx = 300
dy = 300
sc = 1

up = False
down = False
left = False 
right = False

def draw():

    global dx, dy, up, down, left, right, sc, f

    if up:
        dy -= INPUT_MULTIPLIER
    if down: 
        dy += INPUT_MULTIPLIER
    if left:
        dx -= INPUT_MULTIPLIER
    if right:
        dx += INPUT_MULTIPLIER

    background(0)
    rect_mode(CENTER)

    # DISPLACED DRAWING
    translate(dx, dy)
    scale(sc)

    # edges 
    for u, v, w in G.edges(data=True):
        weight = G.edges[u, v]['weight']
        p1 = (nodes[u].x, nodes[u].y)
        p2 = (nodes[v].x, nodes[v].y)
        pm = midpoint(p1, p2)
        
        stroke(100)
        line(p1, p2)

        text_font(f, 10)
        text(str(weight), pm[0], pm[1])
        

    # nodes
    for k, v in nodes.items():
        v.draw(k, f)

def midpoint(a, b): #expects a, b to be tuples
    return (
        (a[0] + b[0])/2,
        (a[1] + b[1])/2
    )

def step():

    filtered = {k: v for k, v in nodes.items() if v.aware > 0}

    for k, v in filtered.items():
        v.run(k)

def mouse_wheel(event):
    global sc 

    y = event.scroll.y

    if y == 1:
        sc *= SCALE_MULTIPLIER
    elif y == -1:
        sc /= SCALE_MULTIPLIER

def key_pressed(event):
    global up, down, left, right

    key = event.key

    if key == "ENTER":
        step()
    elif key == "W":
        up = True
    elif key == "A":
        left = True 
    elif key == "S":
        down = True 
    elif key == "D":
        right = True
    elif key == "R":
        node_init()

def key_released(event):
    global up, down, left, right
    
    key = event.key

    if key == "W":
        up = False
    elif key == "A":
        left = False 
    elif key == "S":
        down = False 
    elif key == "D":
        right = False


run(renderer="vispy")