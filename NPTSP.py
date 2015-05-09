import networkx as nx 
import matplotlib.pyplot as plt
import time
import itertools as ite 
import os

class ArrayUnionFind:
    """Holds the three "arrays" for union find"""
    def __init__(self, S):
        self.group = dict((s,s) for s in S) # group[s] = id of its set
        self.size = dict((s,1) for s in S) # size[s] = size of set s
        self.items = dict((s,[s]) for s in S) # item[s] = list of items in set s
        
def make_union_find(S):
    """Create a union-find data structure"""
    return ArrayUnionFind(S)
    
def find(UF, s):
    """Return the id for the group containing s"""
    return UF.group[s]

def union(UF, a,b):
    """Union the two sets a and b"""
    assert a in UF.items and b in UF.items
    # make a be the smaller set
    if UF.size[a] > UF.size[b]:
        a,b = b,a
    # put the items in a into the larger set b
    for s in UF.items[a]:
        UF.group[s] = b
        UF.items[b].append(s)
    # the new size of b is increased by the size of a
    UF.size[b] += UF.size[a]
    # remove the set a (to save memory)
    del UF.size[a]
    del UF.items[a]


def validColor(G, a, b):
    p = G.node[a]['color'] in G.node[a]['neighbor_color'] and G.node[a]['color']==G.node[b]['color']
    q = G.node[b]['color'] in G.node[b]['neighbor_color'] and G.node[a]['color']==G.node[b]['color']
    return (not p) and (not q)

def addNeighborColor(G, a, b):
    G.node[a]['neighbor_color'].append(G.node[b]['color'])
    G.node[b]['neighbor_color'].append(G.node[a]['color'])

def removeNeighborColor(G, a, b):
    G.node[a]['neighbor_color'].remove(G.node[b]['color'])        #remove neighbor color
    G.node[b]['neighbor_color'].remove(G.node[a]['color']) 

def kruskal_mst(G):
    """Return a minimum spanning tree using kruskal's algorithm"""
    # sort the list of edges in G by their length
    Edges = [(u, v, G[u][v]['weight']) for u,v in G.edges()]
    Edges.sort(cmp=lambda x,y: cmp(x[2],y[2]))

    UF = make_union_find(G.nodes())  # union-find data structure

    # for edges in increasing weight
    mst = [] # list of edges in the mst
    for u,v,d in Edges:
        setu = find(UF, u)
        setv = find(UF, v)
        # if u,v are in different components
        if setu != setv:
            if validColor(G, u, v):
                addNeighborColor(G, u, v)
                mst.append((u,v))
                union(UF, setu, setv)
    return mst




def drawGraph(graph):
    pos=nx.shell_layout(graph)
    redList = []
    blackList = []
    labels = {}
    edgeLabel = {}
    for x in graph.edges():
        #edgeLabel[x]=str(G[x[0]][x[1]]['weight'])
        edgeLabel[x]=str(1)
    for x in xrange(graph.number_of_nodes()):
        labels[x]=x
        if graph.node[x]["color"] == 'R':
            redList.append(x)
        else:
            blackList.append(x)
    nx.draw_networkx_nodes(graph,pos,
                       nodelist=redList,
                       node_color='r',
                       node_size=500,
                   alpha=0.8)
    nx.draw_networkx_nodes(graph,pos,
                       nodelist=blackList,
                       node_color='b',
                       node_size=500,
                   alpha=0.8)
    nx.draw_networkx_labels(graph,pos,labels,font_size=16)
    nx.draw_networkx_edges(graph,pos,width=1.0,alpha=0.5)
    #nx.draw_networkx_edge_labels(G,pos, label=edgeLabel)
    plt.show()
    return edgeLabel


def udah_belom(G):
    for i in G.nodes():
        if len(G.neighbors(i))>2:
            return False
    return True


def cheapestLeafConnection(G, H):
    nodes = H.nodes()
    candidates = []
    tmp_weight = 0
    counter = 0
    while not udah_belom(H):
        #counter = 0
        for x in nodes:
            candidates=[]
            counter += 1
            x_neigh = H.neighbors(x)
            if len(x_neigh) > 2:
                for y in x_neigh:
                    #make a copy of current mst
                    dummyGraph = H.copy()
                    
                    #remove edge
                    removeNeighborColor(dummyGraph, x, y)
                    tmp_weight = G[x][y]['weight']      #save weight
                    dummyGraph.remove_edge(x,y)
    
                    tree = nx.dfs_successors(dummyGraph, x)
                    anak_anak = nx.dfs_predecessors(dummyGraph, x)
                    for anak in anak_anak:
                        if anak not in tree:            #if leaf
                            if validColor(dummyGraph, anak, y):
                                tmp = (anak, y, G[anak][y]['weight'])
                                candidates.append(tmp)
                    dummyGraph.add_edge(x, y, weight = tmp_weight)
                    addNeighborColor(dummyGraph, x, y)

            if len(candidates)>0:
                candidates = sorted(candidates, key = lambda z: z[2])
                fro, tom, wei = candidates[0]
                dummyGraph.add_edge(fro,tom, weight=wei)
                removeNeighborColor(dummyGraph, x, tom)
                dummyGraph.remove_edge(x,tom)
                addNeighborColor(dummyGraph, fro, tom)
                H = dummyGraph.copy()
                #drawHraph(H)    
            elif (counter%10000) ==0:
                if counter%100000==0:
                    print 'no candidates,', counter, ' iterations in Cheapest Leaf Connection'
                #drawGraph(dummyGraph)
                for x in nodes:
                    x_neigh = dummyGraph.neighbors(x)
                    if len(x_neigh)==1:
                        dummyGraph.remove_edge(x, x_neigh[0])
                        removeNeighborColor(dummyGraph, x, x_neigh[0])
                        for y in dummyGraph.neighbors(x_neigh[0]):
                            if validColor(dummyGraph, x, y) and len(dummyGraph.neighbors(y))<3:
                                dummyGraph.add_edge(x,y)
                                addNeighborColor(dummyGraph, x, y)
                                H = dummyGraph.copy()
                                break
                        break
            elif counter == 250001:
                print 'Using Cheapest Leaf Connection failed miserably =('
                #os.system('say "Using candidates failed miserably..."')
                print 'Try using Direct Leaf Connection'
                #os.system('say "Try using direct leaf connection"')
                H = directLeafConnection(G, dummyGraph)
                return H
    return H


def directLeafConnection(G, H):
    nodes = H.nodes()
    counter = 0
    while not udah_belom(H):
        if time.time()-waktu1 > 300:
            return H
        for x in nodes:
            counter += 1
            x_neigh = H.neighbors(x)
            if len(x_neigh) > 2:
                for y in x_neigh:
                    dummyGraph = H.copy()
    
                    dummyGraph.node[x]['neighbor_color'].remove(dummyGraph.node[y]['color'])        #remove neighbor color
                    dummyGraph.node[y]['neighbor_color'].remove(dummyGraph.node[x]['color'])        #remove neighbor color
                    dummyGraph.remove_edge(x,y)
    
                    tree = nx.dfs_successors(dummyGraph, x)
                    anak_anak = nx.dfs_predecessors(dummyGraph, x)
                    for anak in anak_anak:
                        if anak not in tree:
                            if validColor(dummyGraph, anak, y):
                                dummyGraph.add_edge(anak,y, weight=G[anak][y]['weight'])
                                addNeighborColor(dummyGraph, y, anak)
                                H = dummyGraph.copy()
                                #drawHraph(H)
                                break
            if counter%100000==0:
                print 'iteration: ', counter, ' in Direct Leaf Connection'
            if counter == 500001:
                #os.system('say "Redo from scratch"')
                mst = kruskal_mst(G)
                H = G.copy()
                H.remove_edges_from(H.edges())
                H.add_edges_from(mst)

                H = directLeafConnection(G, H)
                return H
    return H


def cheapestSuccessorConnection(G, H):
    nodes = H.nodes()
    candidates = []
    tmp_weight = 0
    counter = 0
    while not udah_belom(H):
        for x in nodes:
            candidates=[]
            counter += 1
            x_neigh = H.neighbors(x)
            if len(x_neigh) > 2:
                for y in x_neigh:
                    dummyGraph = H.copy()
                    #remove edge
                    removeNeighborColor(dummyGraph, x, y)
                    tmp_weight = G[x][y]['weight']      #save weight
                    dummyGraph.remove_edge(x,y)

                    anak_anak = nx.dfs_predecessors(dummyGraph, x)
                    for anak in anak_anak:
                        if validColor(dummyGraph, anak, y):
                            tmp = (anak, y, G[anak][y]['weight'])
                            candidates.append(tmp)
                    dummyGraph.add_edge(x, y, weight = tmp_weight)
                    addNeighborColor(dummyGraph, x, y)

                if len(candidates)>0:
                    candidates = sorted(candidates, key = lambda z: z[2])
                    fro, tom, wei = candidates[0]
                    removeNeighborColor(dummyGraph, x, tom)
                    dummyGraph.remove_edge(x,tom)

                    addNeighborColor(dummyGraph, fro, tom)
                    dummyGraph.add_edge(fro,tom, weight=wei)
                    H = dummyGraph.copy()
            if counter==100001:
                #drawGraph(H)
                print "reached 100000 iterations in Cheapest Successor Connection"
                #os.system('say "reached 100000 iterations in cheapest Successor Connection"')
                print 'Moving on to Cheapest Leaf Connection'
                #os.system('say "Moving on to cheapest Leaf Connection"')
                H = cheapestLeafConnection(G, H)
                return H
    return H


def generateInvalids(G):
    reds, blues = [], []
    for x in G.nodes():
        if G.node[x]['color']=='B':
            blues.append(x)
        else:
            reds.append(x)
    global invalids
    invalids = tuple(ite.permutations(reds, 3)) + tuple(ite.permutations(blues, 3))

def BruteForceMania(G):
    def find_paths(G, start, path, distance):
        # Add way point
        path.append(start)
    
        # Calculate path length from current to last node
        if len(path) > 1:
            distance += G[path[-2]][start]['weight']
    
        # If path contains all cities
        if (len(G.nodes()) == len(path)):
            routes.append([distance, path])
            return
        # Fork paths for all possible cities not yet used
        for city in G.neighbors(start): 
            idx = len(path)
            if (city not in path) and (path[idx-2], path[idx-1], city) not in invalids:
                find_paths(G, city, list(path), distance)

    routes = []
    invalids = ()
    generateInvalids(G)     #generate invalids
    #drawGraph(G)

    for x in G.nodes():
        find_paths(G, x, [], 0)
    routes.sort()

    #if len(routes) != 0:
    #    print "Shortest route: %s" % routes[0]
    #else:
    #    print "FAIL!"
        #os.system('say "Fail!"')

    if len(routes)!=0:
        lst = []
        for i in range(len(routes[0][1])-1):
            lst.append((routes[0][1][i], routes[0][1][i+1]))
        H = G.copy()
        H.remove_edges_from(H.edges())
        H.add_edges_from(lst)
        return H

def strPath(G):
    startEnd = []
    for x in G.nodes():
        if len(G.neighbors(x)) == 1:
            startEnd.append(x)
    if len(startEnd)>2:
        return "No TSP Path"

    start = startEnd[0]
    end = startEnd[1]

    x = start
    result = ''
    path =[]
    path.append(x)
    result+= str(int(x+1))+' '
    while x!= end:
        for i in G.neighbors(x):
            if i not in path:
                x=i
                path.append(x)
                result+= str(int(x+1))+' '
                break
    return result[:len(result)-1]


def distance(G,path):
    distance = 0
    for x in range(len(path)-1):
        distance += int(path[x]) + int(path[x+1])
    return distance


def distanceTwo(G,path1,path2):
    dis1 = distance(G,path1)
    dis2 = distance(G,path2)
    a = '   Distance method 1:' + str(dis1)
    b = '   Distance method 2:' + str(dis2)
    print(a)
    print(b)
    if dis1<dis2:
        atit="   Atit's algorithm win!"
    else:
        atit="   Atit's algorithm lost!"
    print(atit)
    selisih='   Selisih:'+ str(abs(dis1-dis2))
    print(selisih)

    res =a + '\n' +b+ '\n' + atit+ '\n'+ selisih
    return res

def writeOutput(G,t):
    path = strPath(G)
    fout = open('answer/answer.out','a')
    fout1 = open('answer/'+str(t)+'.out','w')

    fout.write(path+'\n')
    fout1.write(path)

    fout.close()
    fout1.close()

os.system('clear')
start = input("Specify your starting test file:")
end = input("Specify your ending test file:")
T = end # number of test cases
# os.system('say "Please enter your input file"')
# baji = int(input('Input file number: '))
for t in xrange(start, T+1):
# while baji != -1:
    print '\n'
    fin = open('instances/' + str(t) + ".in", "r")
    # os.system('say "opening new file"')    
    #fin = open( str(baji) + ".in", "r")
    print("Opening " + str(t) + ".in")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()] 
    c = fin.readline()                                          #color

    G=nx.Graph()
    #make graph
    for i in range(N):              #insert nodes
        G.add_node(i, color=c[i], neighbor_color=[])

    for i in range(N):              #insert edges
        for j in range(N):
            if j>i:                 #avoid duplicate (i-j and j-i)
                G.add_edge(i, j, weight=d[i][j])

    #drawGraph(G)
    waktu1 = time.time()
    if N<0:                        #Threshold for bruteforce
        print 'Trying BruteForce'
        #os.system('say "Trying BruteForce"')
        H = BruteForceMania(G)
    else:
        print "Trying cheapest Successor Connection"
        #os.system('say "Trying cheapest Successor Connection"' )
        mst = kruskal_mst(G)
        H = G.copy()
        H.remove_edges_from(H.edges())
        H.add_edges_from(mst)
        H = cheapestSuccessorConnection(G, H)
    drawGraph(H)
    writeOutput(H,t)



    print("Finished processing file " + str(t) + ".in")
    print '-------------------------------------------'
    #os.system('say "E Z"')
    #os.system('say "Its done. I am ready for your next challenge!"')


    # os.system('say "Please enter your input file"')
    # baji = int(input('Input file number: '))
    # if baji== -1:
        # break