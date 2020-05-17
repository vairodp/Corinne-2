from fsa import FSA


class CFSM(FSA):
    """
        This class implement the communicating finite-state machine (CFSM).
        A CFSM is a Finite State Machine where labels are in the
        form of 'A B!m' or 'A B?m' (with A!=B)
    """
    def __init__(self, states: set, labels: set, edges: set, s0: str, participants: set):
        super().__init__(states, labels, edges, s0)
        self.participants = participants
    
    def __get_participants_and_message_from_label__(self, label):
        sender, receiver_message = label.split(' ')
        if '?' in receiver_message:  # case: A B?m
            receiver, message = receiver_message.split('?')
        else:  # case A B!m
            receiver, message = receiver_message.split('!')
        return sender.strip(), receiver.strip(), message.strip()
    
    def __transition_exist__(self, state, label):
        """ If a transition δ(state, label, state2) exist
            return state2, otherwise False. """
        for edge in self.edges:
            if edge[0] == state and edge[1] == label:
                return edge[2]
        return False
    
    def minimization(self):
        """
            Implement an algorithm of minimization for the Communicating FSM.
            This is based on the Table filling method (Myhill Nerode Theorem).
        """
        # create every pair of nodes, where the pair (i,j) is the same pair of (j,i)
        # and can't be exist a pair (i,j) with i == j
        self.states = set(map(str, self.states))  # TODO verify why self.states are integer in this point
        nodes_pairs = set()
        for i in self.states:
            for j in self.states:
                if i != j and not (i, j) in nodes_pairs and not (j, i) in nodes_pairs:
                    nodes_pairs.add((i, j))
        """
        NOTE: from the moment we're dealing with FSA with a partial transition
        function (not all transitions are defined for every node), the algorithm
        has been adapted. So, in the second step of the algorithm for every pair of
        nodes (i,j) we'll check if δ(i,label) and δ(j,label) exist, and we act
        accordingly to every possible case.
        """
        distinguishable_states = set()
        stop = True
        # a boolean to stop the algorithm if after a cycle
        # no distinguishable pair of node was founded.
        while stop:
            stop = False
            # at every cycle of the algorithm we delete every
            # distinguishable states from the set of possible nodes pairs.
            nodes_pairs = nodes_pairs.difference(distinguishable_states)
            for node in nodes_pairs:
                for label in self.labels:
                    i = self.__transition_exist__(node[0], label)
                    j = self.__transition_exist__(node[1], label)
                    if i and j:  # both δ(i,label) and δ(j,label) exist
                        if i != j:  # both transitions are going in different nodes
                            # check if they are going in a distinguishable pair of nodes
                            if (i, j) in distinguishable_states or (j, i) in distinguishable_states:
                                stop = True
                                distinguishable_states.add((node[0], node[1]))
                                break
                    elif i or j:  # one of δ(i,label) or δ(j,label) exist
                        stop = True
                        distinguishable_states.add((node[0], node[1]))
                        break
                    # if both transitions don't exist, nothing to do
        undistinguished_states = set()
        for pair in nodes_pairs:
            undistinguished_states.add(pair[0])
            undistinguished_states.add(pair[1])
        
        self.states = self.states.difference(undistinguished_states)
        
        merge_node = ""
        for state in undistinguished_states:
            merge_node += state + ','
        merge_node = merge_node[:-1]
        if merge_node:
            self.states.add(merge_node)
        
        new_edges = set()
        for edge in self.edges:
            node1 = edge[0] in undistinguished_states
            node2 = edge[2] in undistinguished_states
            if not (node1 and node2):  # node1 NAND node2
                if node1:
                    new_edges.add((merge_node, edge[1], edge[2], edge[3], edge[4], edge[5]))
                elif node2:
                    new_edges.add((edge[0], edge[1], merge_node, edge[3], edge[4], edge[5]))
                else:
                    new_edges.add(edge)
            else:
                new_edges.add((merge_node, edge[1], merge_node, edge[3], edge[4], edge[5]))
        self.edges = new_edges
