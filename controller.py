import os
from graphviz import render, Digraph, view
from cfsm import CFSM
from global_graph_parser.main import main as global_graph_parser
from dot_parser.main import main
from dot_parser.domitilla_converter import domitilla_converter
from dot_parser.MyErrorListener import parseError
from dot_parser.MyVisitor import ForkStatementDetected


class Controller:
    ca_dict = {}

    def get_participants(self, graph_name):
        """ Return participants of a given graph """
        return self.ca_dict.get(graph_name).participants
    
    def get_all_ca(self):
        """ Return all the opened graphs """
        return self.ca_dict
    
    def get_start_node(self, graph_name):
        """ Return the start node of a given graph """
        return self.ca_dict.get(graph_name).s0
    
    def get_states(self, graph_name):
        """ Return the states of a given graph """
        return self.ca_dict.get(graph_name).states
    
    def get_edges(self, graph_name):
        """ Return the edges of a given graph """
        return self.ca_dict.get(graph_name).edges
    
    def get_labels(self, graph_name):
        """ Return the labels of a given graph """
        return self.ca_dict.get(graph_name).labels
    
    def check_for_epsilon_moves(self, graph_name):
        for edge in self.ca_dict.get(graph_name).edges:
            if edge[1] == "":
                return "Yes"
        return "No"
    
    def GGparser(self, path_file, path_store):
        """ Parser a Chorgram file and create a converted
            version (DOT) in a given path.
        """
        # read the file and convert in DOT
        message, path = global_graph_parser(path_file, path_store)
        # parse the new DOT file and store the graph
        result = self.DOTparser(path)
        # return a log message and the name of the graph
        return message, result[2]
    
    def DOTparser(self, path_file):
        """ Parser a DOT files, check if it was a Domitilla graph
            and fill a Choreography Automata (CA) struct. """
        try:
            ca, domi_bool, graph_name = main(path_file)
        except (parseError, ForkStatementDetected) as e:
            return False, e.message  # return eventually an error message
        else:
            # store the CA in a dictionary { 'graph_name' : CA }
            self.ca_dict.update({graph_name: ca})
            # return a boolean for Domitilla graphs, a log message
            # and the name of the graph
            return domi_bool, ["Read Successfully " + path_file], graph_name
    
    def DomitillaConverter(self, graph_name, path_file, path_store):
        """ Convert a Domitilla Graph, previously opened and stored.
            Check /dot_parser/domitilla_visitor.py """
        ca, message = domitilla_converter(self.ca_dict.get(graph_name), path_file, path_store)
        self.ca_dict.update({graph_name: ca})
        return message
    
    def remove_record(self, graph_name):
        """ Remove a graph from the opened graphs dictionary (self.ca_dict)"""
        self.ca_dict.pop(graph_name)
    
    def render(self, path_file, extension,V_rend_on_default_image_viewer):
        try:
            main(path_file)  # check for errors
        except (parseError, ForkStatementDetected) as e:
            print("non riesco a creare il render")
            return e.message[0] + " " + e.message[1]  # return eventually an error message
        else:
            #V voglio mettere che lo apre se glielo dico io,altirmenti mi rendera quello
            #che volgio    
            save_path = render('dot', extension, path_file)

            if V_rend_on_default_image_viewer == True:
                view(save_path)  # open the default image viewer
            return save_path

    def make_product(self, graph_name1, graph_name2, path_to_store):
        """ Make the product of two choreography automata (ca1, ca2),
            building a c-automaton corresponding to the concurrent
            execution of the two original c-automata. """
        
        # get the two choreography automaton from graphs name
        ca1 = self.ca_dict.get(graph_name1)
        ca2 = self.ca_dict.get(graph_name2)
        # check if the participants are disjoint,
        if ca1.participants.intersection(ca2.participants):
            return ["[ERROR] participants are not disjoint"]
        # if the user didn't add a .gv extension to the name of
        # product graph, we'll add it
        if not path_to_store.endswith('.gv'):
            path_to_store += '.gv'
        # get the name from the path
        path_splitted = os.path.split(path_to_store)
        graph_name = path_splitted[1].split('.')
        # initializes graph
        g = Digraph(graph_name[0])
        g.node('s0', label="", shape='none', height='0', width='0')
        start_node = ca1.s0 + ',' + ca2.s0
        g.edge('s0', start_node)
        # Build the product graph
        # NOTE: for each edge
        # edge[0] == sender node
        # edge[1] == label
        # edge[2] == receiver node
        for i in ca1.states:
            for j in ca2.states:
                # current node we re considering
                node = str(i) + ',' + str(j)
                # set j, and look for some edges from i to other nodes
                for edge in ca1.edges:
                    if edge[0] == i:
                        g.edge(node, str(edge[2]) + ',' + str(j), label=str(edge[1]))
                # set i, and look for some edges from j to other nodes
                for edge in ca2.edges:
                    if edge[0] == j:
                        g.edge(node, str(i) + ',' + str(edge[2]), label=str(edge[1]))
        # draw and save the graph
        g.save(path_to_store)
        # parser the product graph and
        # store the relative CA
        result = self.DOTparser(path_to_store)
        # return a message, and
        # the graph name just created
        return ["[CREATED] " + path_to_store]
    
    def synchronize(self, graph_name_to_sync, interface1, interface2, path_to_store):
        """
            Remove a pair of (compatible) roles by transforming them into forwarders.
            e.g.: a synchronization over H and K removes participants H and K and
            sends each message originally sent to H to whoever K used to send the
            same message, and vice versa.
        """
        # get the choreography automaton from graph name
        ca = self.ca_dict.get(graph_name_to_sync)
        # check if interfaces aren't the same
        if interface1 == interface2:
            return ["[ERROR] you selected the same participant for both interfaces"]
        # if the user didn't add a .gv extension to the name of
        # sync graph, we'll add it
        if not path_to_store.endswith('.gv'):
            path_to_store += '.gv'
        # get the name from the path
        path_splitted = os.path.split(path_to_store)
        graph_name = path_splitted[1].split('.')
        # initializes graph
        g = Digraph(graph_name[0])
        g.node('s0', label="", shape='none', height='0', width='0')
        g.edge('s0', ca.s0)
        #
        # NOTE: each edge in ca.edges contains a 6-uple like this:
        # (source_node, label, dest_node, sender, receiver, message)
        #
        # ------------ STEP (1) -----------------
        # each transition (p, A -> H: m, q) is removed, and for each
        # transition (q, K -> B: m, r) a transition (p, A -> B: m, r)
        # is added, and similarly by swapping H and K
        new_edges = set()
        edges_to_remove = set()
        for i in ca.edges:
            if i[4] == interface1:
                edges_to_remove.add(i)
                for j in ca.edges:
                    if j[0] == i[2] and j[3] == interface2 and j[5] == i[5] and i[3] != j[4]:
                        edges_to_remove.add(i)
                        label = i[3] + '->' + j[4] + ':' + i[5]
                        new_edges.add((i[0], label, j[2], i[3], j[4], i[5]))
            
            if i[4] == interface2:
                for j in ca.edges:
                    if j[0] == i[2] and j[3] == interface1 and j[5] == i[5] and i[3] != j[4]:
                        edges_to_remove.add(i)
                        label = i[3] + '->' + j[4] + ':' + i[5]
                        new_edges.add((i[0], label, j[2], i[3], j[4], i[5]))
        ca.edges = ca.edges.difference(edges_to_remove)
        ca.edges = ca.edges.union(new_edges)
        # ------------ STEP (2) -----------------
        # Transitions involving neither H nor K are preserved,
        # whereas all other transitions are removed
        edges_to_remove.clear()
        for i in ca.edges:
            if i[3] == interface1 or i[3] == interface2 or i[4] == interface1 or i[4] == interface2:
                edges_to_remove.add(i)
        ca.edges = ca.edges.difference(edges_to_remove)
        # ------------ STEP (3) -----------------
        # States and transitions unreachable from the initial
        # state are removed.
        ca.delete_unreachable_nodes()
        for edge in ca.edges:
            g.edge(edge[0], edge[2], label=str(edge[1]))
        # draw and save the graph
        g.save(path_to_store)
        # parser the product graph and
        # store the relative CA
        result = self.DOTparser(path_to_store)
        return ["[CREATED] " + path_to_store]
    
    def projection(self, graph_name, participant, path_to_store):
        """
            The projection of a c-automaton on a participant A
            is a CFSM, obtained by minimising the c-automaton
            after updating the labels.
        """
        # get the choreography automaton from graph name
        ca = self.ca_dict.get(graph_name)
        # if the user didn't add a .gv extension to the name of
        # sync graph, we'll add it
        if not path_to_store.endswith('.gv'):
            path_to_store += '.gv'
        # get the name from the path
        path_splitted = os.path.split(path_to_store)
        graph_name = path_splitted[1].split('.')
        # initializes graph
        g = Digraph(graph_name[0])
        # NOTE: each edge in ca.edges contains a 6-uple like this:
        # (source_node, label, dest_node, sender, receiver, message)
        new_edges = set()
        new_labels = set()
        for edge in ca.edges:
            # if the participant is the sender
            if edge[3] == participant:
                label = participant + ' ' + edge[4] + '!' + edge[5]
                new_edges.add((edge[0], label, edge[2]))
                new_labels.add(label)
            # if the participant is the receiver
            elif edge[4] == participant:
                label = edge[3] + ' ' + participant + '?' + edge[5]
                new_edges.add((edge[0], label, edge[2]))
                new_labels.add(label)
            # in all the other cases, empty_label edges
            else:
                new_edges.add((edge[0], "", edge[2]))
        
        c = CFSM(ca.states, new_labels, new_edges, ca.s0, ca.participants)
        c.delete_epsilon_moves()
        c.minimization()
        
        for edge in c.edges:
            g.edge(str(edge[0]), str(edge[2]), label=edge[1])
        # draw and save the graph
        g.save(path_to_store)
        
        return ["[CREATED] " + path_to_store]
