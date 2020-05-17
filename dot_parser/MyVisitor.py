from chor_auto import ChoreographyAutomata
from .utils import get_string_from_tokens, get_interaction_string
from .DOTParser import DOTParser
from .DOTVisitor import DOTVisitor


class ForkStatementDetected(Exception):
    def __init__(self):
        self.message = ["[WARNING] Fork founded! I can't accept that"]
    

class MyVisitor(DOTVisitor):
    """
    This class is based on the ANTLR visitor class.
    It visit each node of the parse tree and produce
    a choreography automata struct for the input graph.
    It also verify if the input graph is a Domitilla
    graph, so we'll check for :
        - labelled nodes;
        - choice node;
        - fork node (it raise an exception);

    Return a 3-tuple which contains a choreography
    automata struct, a boolean value(for domitilla)
    and the name of the graph
    """
    def __init__(self):
        self.states = set()
        self.labels = set()
        self.edges = set()
        self.s0 = None
        self.participants = set()
        self.domitilla = 0
    
    # Visit a parse tree produced by DOTParser#graph.
    def visitGraph(self, ctx:DOTParser.GraphContext):
        self.visitChildren(ctx)
        graph_name = get_string_from_tokens(ctx.string())
        if self.s0 is not None:
            start_node = self.s0
        else:
            start_node = min(self.states)
        ca = ChoreographyAutomata(self.states, self.labels,
                                  self.edges, start_node,
                                  self.participants)
        
        return ca, self.domitilla, graph_name

    # Visit a parse tree produced by DOTParser#stmt_list.
    def visitStmt_list(self, ctx:DOTParser.Stmt_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#stmt.
    def visitStmt(self, ctx:DOTParser.StmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#node.
    def visitNode(self, ctx:DOTParser.NodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#edge.
    def visitEdge(self, ctx:DOTParser.EdgeContext):
        # get the nodes
        nodes = ctx.id_node()
        source_node = nodes[0]
        dest_node = nodes[1]
      
        if source_node.Number() is not None:
            source_str = source_node.Number().getText()
        else:
            source_str = get_string_from_tokens(source_node.string())
            
        if dest_node.Number() is not None:
            dest_str = dest_node.Number().getText()
        else:
            dest_str = get_string_from_tokens(dest_node.string())

        # check for label
        if ctx.label() is not None:
            if isinstance(ctx.label(), DOTParser.InteractionContext):
                result = get_interaction_string(ctx.label())
                # add the edge with label
                # (source_node, label, dest_node, sender, receiver, message)
                self.edges.add((source_str, result[3], dest_str, result[0], result[1], result[2]))
        else:
            # add a no-label edge
            self.edges.add((source_str, "", dest_str, "", "", ""))

        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#start_node.
    def visitStart_node(self, ctx: DOTParser.Start_nodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#start_edge.
    def visitStart_edge(self, ctx: DOTParser.Start_edgeContext):
        if ctx.Number() is not None:
            start_node = ctx.Number().getText()
        else:
            start_node = get_string_from_tokens(ctx.string())
        self.s0 = start_node
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#attr_list.
    def visitAttr_list(self, ctx:DOTParser.Attr_listContext):
        if ctx.label() is not None:
            if isinstance(ctx.label(), DOTParser.ForkContext):
                raise ForkStatementDetected
            else:
                self.domitilla = True
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#id_node.
    def visitId_node(self, ctx: DOTParser.Id_nodeContext):
        if ctx.Number() is not None:
            self.states.add(ctx.Number().getText())
        else:
            self.states.add(get_string_from_tokens(ctx.string()))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#string.
    def visitString(self, ctx: DOTParser.StringContext):
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by DOTParser#interaction.
    def visitInteraction(self, ctx:DOTParser.InteractionContext):
        # add participants
        self.participants.add(str(ctx.Uppercase_letter(0)))
        self.participants.add(str(ctx.Uppercase_letter(1)))
        interaction_string = get_interaction_string(ctx)
        # add the label
        self.labels.add(interaction_string[3])
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#cfsm_interaction.
    def visitCfsm_interaction(self, ctx: DOTParser.Cfsm_interactionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#choice.
    def visitChoice(self, ctx:DOTParser.ChoiceContext):
        self.domitilla = True
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DOTParser#Fork.
    def visitFork(self, ctx:DOTParser.ForkContext):
        raise ForkStatementDetected
