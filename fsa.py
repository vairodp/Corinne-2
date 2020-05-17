from abc import ABC, abstractmethod


class FSA(ABC):
    """
        This class is an implementation of an usual Finite-state automata (FSA),
        with a finite set of states, set of labels, set of transitions (edges)
        and one initial state (s0)
    """
    
    def __init__(self, states: set, labels: set, edges: set, s0: str):
        self.states = states
        self.labels = labels
        self.edges = edges
        self.s0 = s0
    
    def __e_closure__(self, nodes):
        """
        Given a set of nodes, return the ∈-closure of the set:
        a set of reachable nodes, starting from a node of the
        given set and with only empty label moves.
        """
        result = set(nodes)
        stack_nodes = [nodes]
        while len(stack_nodes) > 0:
            current_node = stack_nodes.pop()
            for node in current_node:
                for edge in self.edges:
                    if edge[0] == node and edge[1] == "":
                        if not edge[2] in result:
                            result.add(edge[2])
                            stack_nodes.append([edge[2]])
        return result
    
    def __label_closure__(self, node, label):
        """
        Given a node and a label return a set of
        reachable nodes, starting from the given
        node and with only the given label moves.
        """
        result = set()
        for edge in self.edges:
            if edge[0] == node and edge[1] == label:
                result.add(edge[2])
        return result
    
    def delete_epsilon_moves(self):
        """ delete epsilon (empty) moves from the FSA """
        
        # Take ∈-closure of the start node as beginning state
        start_node = self.__e_closure__(self.s0)
        # a stack through iterate
        stack_nodes = [start_node]
        # a dict to store new nodes, in the form of:
        # { 0  : set_of_nodes(0,1,..),
        #   1  : set_of_nodes(2,5,..),
        #  ... : ,,, }
        final_states = {}
        # a count to enumerate new nodes
        count = 0
        final_states[count] = start_node
        # a list to store new edges
        final_edges = []
        
        while len(stack_nodes) > 0:
            current_node = stack_nodes.pop()
            # find ID of the node
            id_node = ""
            for key, value in final_states.items():
                if value == current_node:
                    id_node = str(key)
            
            for label in self.labels:
                new_node = set()
                for node in current_node:
                    # find the set of nodes reachable from node with label
                    label_closure = self.__label_closure__(node, label)
                    # now from this set, find a set of nodes reachable with
                    # epsilon moves (e-closure)
                    if len(label_closure):
                        new_node = new_node.union(self.__e_closure__(label_closure))
                if len(new_node):
                    sender, receiver, message = self.__get_participants_and_message_from_label__(label)
                    if not new_node in final_states.values():
                        count += 1
                        final_states[count] = new_node
                        stack_nodes.append(new_node)
                        final_edges.append((id_node, label, str(count), sender, receiver, message))
                    else:
                        for k, value in final_states.items():
                            if value == new_node:
                                final_edges.append((id_node, label, str(k), sender, receiver, message))
        self.edges = set(final_edges)
        self.states = set(final_states.keys())
    
    def delete_unreachable_nodes(self):
        """ delete unreachable nodes from the initial state s0 """
        visited_edges = set()
        visited_nodes = set()
        stack = []
        
        # add the start point
        visited_nodes.add(self.s0)
        stack.append(self.s0)
        
        while len(stack) > 0:
            current_node = stack.pop()
            for edge in self.edges:
                if edge[0] == current_node:
                    # add the edge to the result graph
                    visited_edges.add(edge)
                    # if i didn't already visit this node
                    if not edge[2] in stack and not edge[2] in visited_nodes:
                        # add the node to the result graph
                        visited_nodes.add(edge[2])
                        # add the node in the stack
                        # to visit later
                        stack.append(edge[2])
        self.edges = visited_edges
        self.states = visited_nodes
    
    @abstractmethod
    def __get_participants_and_message_from_label__(self, label):
        pass
