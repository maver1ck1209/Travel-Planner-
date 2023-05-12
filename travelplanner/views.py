from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import sys
# Create your views here.
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    s = " -> ".join(reversed(path))
    return s



@login_required(login_url='/login')
def index(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            #EMAIL
            htmly = get_template('Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            #Redirect to login
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form":form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            messages.error(request, f'account does not exit plz register')
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

def pyt(request):
    if request.method=='POST':
        s = request.POST['Source']
        d = request.POST['Destination']
        o = request.POST['Optimize Using']
        nodes = ["Chennai, India", 
         "Montreal, Canada", 
         "Dubai, UAE", 
         "Maturin, Venezuela", 
         "Los Angeles, USA",
         "New York, USA",
         "Waterloo, Canada",
         "Longford, UK",
         "Paris, France",
         "Frankfurt, Germany",
         "Dublin, Ireland",
         "London, UK",
         "Tokyo, Japan",
         "Shanghai, China",
         "Singapore",
         "Sidney, Australia",
         "Cairo, Egypt",
         "Toronto, Canada",
         "Texas, USA",
         "Stanford, USA"]

        init_graph = {}
        for node in nodes:
            init_graph[node] = {}

        if o == 'Distance':
            # Creating the dataset based on distance (in km)
            init_graph["Chennai, India"]["Longford, UK"] = 8228
            init_graph["Longford, UK"]["Montreal, Canada"] = 3230
            init_graph["Dubai, UAE"]["Shanghai, China"] = 6422
            init_graph["Shanghai, China"]["Tokyo, Japan"] = 1758
            init_graph["Tokyo, Japan"]["Singapore"] = 6892
            init_graph["Singapore"]["Sidney, Australia"] = 6302
            init_graph["Sidney, Australia"]["Stanford, USA"] = 11940
            init_graph["Stanford, USA"]["Texas, USA"] = 2506
            init_graph["Texas, USA"]["Los Angeles, USA"] = 2005
            init_graph["Los Angeles, USA"]["New York, USA"] = 3936
            init_graph["New York, USA"]["Toronto, Canada"] = 789
            init_graph["Toronto, Canada"]["Waterloo, Canada"] = 113
            init_graph["Waterloo, Canada"]["London, UK"] = 5793
            init_graph["London, UK"]["Paris, France"] = 475
            init_graph["Paris, France"]["Frankfurt, Germany"] = 572
            init_graph["Frankfurt, Germany"]["Dublin, Ireland"] = 1378
            init_graph["Dublin, Ireland"]["Longford, UK"] = 111
            init_graph["Longford, UK"]["New York, USA"] = 3109
            init_graph["New York, USA"]["Maturin, Venezuela"] = 2412
            init_graph["Maturin, Venezuela"]["Frankfurt, Germany"] = 8407
            init_graph["Frankfurt, Germany"]["Cairo, Egypt"] = 4872
            init_graph["Cairo, Egypt"]["Chennai, India"] = 2920
        if o == 'Cost':
            # Creating the dataset based on cost (in Rupee)
            init_graph["Chennai, India"]["Longford, UK"] = 76932
            init_graph["Longford, UK"]["Montreal, Canada"] = 58639
            init_graph["Dubai, UAE"]["Shanghai, China"] = 63831
            init_graph["Shanghai, China"]["Tokyo, Japan"] = 73752
            init_graph["Tokyo, Japan"]["Singapore"] = 33092
            init_graph["Singapore"]["Sidney, Australia"] = 34940
            init_graph["Sidney, Australia"]["Stanford, USA"] = 93937
            init_graph["Stanford, USA"]["Texas, USA"] = 13139
            init_graph["Texas, USA"]["Los Angeles, USA"] = 9390
            init_graph["Los Angeles, USA"]["New York, USA"] = 14811
            init_graph["New York, USA"]["Toronto, Canada"] = 16638
            init_graph["Toronto, Canada"]["Waterloo, Canada"] = 1526
            init_graph["Waterloo, Canada"]["London, UK"] = 79023
            init_graph["London, UK"]["Paris, France"] = 6393
            init_graph["Paris, France"]["Frankfurt, Germany"] = 13293
            init_graph["Frankfurt, Germany"]["Dublin, Ireland"] = 11068
            init_graph["Dublin, Ireland"]["Longford, UK"] = 6722
            init_graph["Longford, UK"]["New York, USA"] = 52956
            init_graph["New York, USA"]["Maturin, Venezuela"] = 91633
            init_graph["Maturin, Venezuela"]["Frankfurt, Germany"] = 67062
            init_graph["Frankfurt, Germany"]["Cairo, Egypt"] = 36931
            init_graph["Cairo, Egypt"]["Chennai, India"] = 33087
        graph = Graph(nodes, init_graph)
        previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=s)
        m = print_result(previous_nodes, shortest_path, start_node=s, target_node=d)
        request.session['output'] = m
        return render(request, 'pytop.html', {'output':m})
    else:
        return render(request, 'pyt.html')
