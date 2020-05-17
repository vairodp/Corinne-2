import os
from graphviz import Digraph
from chor_auto import ChoreographyAutomata
from .utils import extract_name, get_string_from_tokens, get_interaction_string
from .DOTParser import DOTParser
from .DOTVisitor import DOTVisitor


class DomitillaVisitor(DOTVisitor):
    """
    This class is based on the ANTLR visitor class;
    """
    
    def __init__(self, ca: ChoreographyAutomata, path_file, path_store):
        self.path_store = path_store
        self.ca = ca  # choreography automata
        self.graph_name = extract_name(path_file)
        self.g = Digraph(self.graph_name)  # initializes graph
    
    def __project_labels__(self, node, interaction_struct):
        """
            Aim of this function is to project label
            (which in Domitilla are stored on nodes)
            on edges. For example, if there is a node
            like this:

            -----> [A -> B : m] ----->

            we'll project the label to the incoming edges
            of the node, so it will become:

            ---A->B:m---> [ ]  ------->
        """
        incoming_edges = set()
        # identify incoming edges
        for edge in self.ca.edges:
            if edge[2] == node:
                incoming_edges.add(edge)
        
        # Edges are stored in a set, so we can't
        # update them directly, we have to remove
        # the old ones and add the new ones
        
        # remove old edges
        self.ca.edges -= incoming_edges
        # update edges with the interaction label
        for i in incoming_edges:
            # (source_node, label, dest_node, sender, receiver, message)
            self.ca.edges.add((i[0], interaction_struct[3], i[2], interaction_struct[0],
                               interaction_struct[1], interaction_struct[2]))
    
    def visitGraph(self, ctx: DOTParser.GraphContext):
        self.visitChildren(ctx)
        self.g.node('s0', label="", shape='none', height='0', width='0')
        self.g.edge('s0', self.ca.s0)
        
        self.ca.delete_epsilon_moves()
        for edge in self.ca.edges:
            self.g.edge(str(edge[0]), str(edge[2]), label=edge[1])
        
        new_path = os.path.join(self.path_store, "[Converted]" + str(self.graph_name) + ".gv")
        # save the graph
        self.g.save(new_path)
        
        # return CA and path of the converted graph
        return self.ca, new_path
    
    def visitNode(self, ctx: DOTParser.NodeContext):
        # get the attributes list node
        attrs = ctx.attr_list()
        # get the node
        node = ctx.id_node()
        if node.Number() is not None:
            node_id = node.Number().getText()
        else:
            node_id = get_string_from_tokens(node.string())
        
        for i in attrs:
            # check for labelled edge
            label_context = i.label()
            if label_context is not None:
                # if we find a labelled edge
                if isinstance(label_context, DOTParser.InteractionContext):
                    DomitillaVisitor.__project_labels__(self, node_id,
                                                        get_interaction_string(label_context))
        return self.visitChildren(ctx)
