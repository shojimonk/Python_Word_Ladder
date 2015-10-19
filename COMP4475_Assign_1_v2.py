# John Simko
# COMP 4475 FA  - 2015

import Queue

class Node(object):
    '''
    stores nodes of a graph. self.key is the identifier, and
    self.value is a list of nodes 1 step away. self.distance
    is used to track the number of steps from the root it is
    and self.parent points to the next node towards the root
    '''

    def __init__(self, key):
        self.key = key
        self.value = []
        self.distance = 999
        self.parent = None

    def addChild(self, value):
        ''' appends a new child node to the list of nodes '''
        self.value.append(value)

    def getDiff(self, word):
        '''
        returns number of characters that match in
        two strings. matches must be in correct position
        as well
        '''
        loop = (len(self.key) - 1)
        matches = 0
        while loop >= 0:
            if self.key[loop] == word[loop]:
                matches += 1
            loop -= 1
            continue
        return matches

def breadthFirst(start, end):
    '''
    implements a breadth first search of the graph of nodes.
    starts at a given root node, and uses a queue to search
    all equidistant nodes before going further. (ignores
    nodes that have already been visited earlier)
    '''
    global q
    start.distance = 0
    q.put(start)
    while not q.empty():
        curr = q.get()
        if curr.key == end.key: #goal found
            return curr
        for child in curr.value:
            if child.distance == 999:
                child.distance = curr.distance + 1
                child.parent = curr
                q.put(child)    #if not at solution, add children to queue
                
def import_dict(fname):
    ''' reads from file and returns each file line in a list '''
    #fname = "dictionary.txt"
    filein = open(fname)
    temp_dict = filein.read()
    dict_list = temp_dict.splitlines()
    print "infunc:", len(dict_list)
    return dict_list

def create_graph(start):
    '''
    finds and stores all nodes that are adjacent to each
    node, creating a "graph" of the nodes that can be
    traversed.
    '''
    percent = len(node_dict) // 50
    count1 = 0
    count2 = 0
    print "Nodes to Graph:", len(node_dict)
    for temp in node_dict:
        count1 += 1
        if(count1 >= percent):
            count2+=1
            print count2*2, "% completed..."
            count1 = 0
        for each in node_dict:
            if (temp.key == each.key): continue
            if temp.getDiff(each.key) == (len(temp.key) - 1):
                temp.addChild(each)

def nodify(start):
    '''
    takes the root word of a new wordpath and creates a node
    list entry for each word in the global dict_list that
    matches the root word in length.
    '''
    length = len(start)
    for each in dict_list:
        if len(each) != length: continue
        temp = Node(each)
        temp.distance = 999
        node_dict.append(temp)
        del temp
        continue

def node_reference(in_1, in_2):
    '''
    Takes user input words and matches to node keys.
    This also verifies that the given start and
    end words are in the loaded dictionary.
    '''
    global start_node
    global end_node
    for each in node_dict:
        if each.key == in_1:
            start_node = each
        if each.key == in_2:
            end_node = each
    if (start_node is None) or (end_node is None):            
        print "Error, invalid word given!"
        quit()
    elif start_node == end_node:
        print "Start and end are the same. Path is 1:", start_node.key
    else: print "good inputs. continuing."

def startup():
    '''
    (re-)initializes variables and loops for multiple
    user graph searches without requiring a restart
    of the program.
    '''
    global node_dict
    global dict_list
    global path
    global start_node
    global end_node
    control_len = 99

    print "Welcome to my Word Ladder solver!"
    print "Unfortunately, this solver runs in O(n^2) time."
    print "So be prepared for a wait when running searches"
    print "on any 5-11 letter words, as there are many...\n"

    fileName = raw_input('Please Enter the dictionary filename: ')
    
    while True:
        in_1 = raw_input('Enter your starting word!: ')
        in_2 = raw_input('Enter your ending word!: ')
        start_node = None
        end_node = None
        path = []
        del(node_dict)
        node_dict = []
        dict_list = import_dict(fileName)
        control_len = len(in_1)
        print "setting up nodes for", control_len, "letter words..."
        nodify(in_1)
        node_reference(in_1, in_2)
        if (start_node is None) or (end_node is None):
            print "error using no_reference."
            quit
        print "creating graph... (this part takes the longest...)"
        create_graph(in_1)
        print "done graphing. searching for paths..."
        
        end = breadthFirst(start_node, end_node)
        if end is None:
            print "No Path exists!"
            
        else:
            print "Path found!"
            while True:
                path.append(end.key)
                if(end.parent is not None):
                    end = end.parent
                else: break
            path.reverse()
            print "Word path is:", path
            again = raw_input('Would you like to enter new values?: ')
            if (again.upper() == "Y") or (again.upper() == "YES"):
                continue
            else: break
    print "Thanks for using my Word Ladder!"
    quit

q = Queue.Queue()
path = []
again = ""
node_dict = []
dict_list = []
start_node = None
end_node = None
startup()
