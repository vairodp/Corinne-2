# Generated from DOT.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DOTParser import DOTParser
else:
    from DOTParser import DOTParser

# This class defines a complete listener for a parse tree produced by DOTParser.
class DOTListener(ParseTreeListener):

    # Enter a parse tree produced by DOTParser#graph.
    def enterGraph(self, ctx:DOTParser.GraphContext):
        pass

    # Exit a parse tree produced by DOTParser#graph.
    def exitGraph(self, ctx:DOTParser.GraphContext):
        pass


    # Enter a parse tree produced by DOTParser#stmt_list.
    def enterStmt_list(self, ctx:DOTParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by DOTParser#stmt_list.
    def exitStmt_list(self, ctx:DOTParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by DOTParser#stmt.
    def enterStmt(self, ctx:DOTParser.StmtContext):
        pass

    # Exit a parse tree produced by DOTParser#stmt.
    def exitStmt(self, ctx:DOTParser.StmtContext):
        pass


    # Enter a parse tree produced by DOTParser#node.
    def enterNode(self, ctx:DOTParser.NodeContext):
        pass

    # Exit a parse tree produced by DOTParser#node.
    def exitNode(self, ctx:DOTParser.NodeContext):
        pass


    # Enter a parse tree produced by DOTParser#edge.
    def enterEdge(self, ctx:DOTParser.EdgeContext):
        pass

    # Exit a parse tree produced by DOTParser#edge.
    def exitEdge(self, ctx:DOTParser.EdgeContext):
        pass


    # Enter a parse tree produced by DOTParser#start_node.
    def enterStart_node(self, ctx:DOTParser.Start_nodeContext):
        pass

    # Exit a parse tree produced by DOTParser#start_node.
    def exitStart_node(self, ctx:DOTParser.Start_nodeContext):
        pass


    # Enter a parse tree produced by DOTParser#start_edge.
    def enterStart_edge(self, ctx:DOTParser.Start_edgeContext):
        pass

    # Exit a parse tree produced by DOTParser#start_edge.
    def exitStart_edge(self, ctx:DOTParser.Start_edgeContext):
        pass


    # Enter a parse tree produced by DOTParser#attr_list.
    def enterAttr_list(self, ctx:DOTParser.Attr_listContext):
        pass

    # Exit a parse tree produced by DOTParser#attr_list.
    def exitAttr_list(self, ctx:DOTParser.Attr_listContext):
        pass


    # Enter a parse tree produced by DOTParser#id_node.
    def enterId_node(self, ctx:DOTParser.Id_nodeContext):
        pass

    # Exit a parse tree produced by DOTParser#id_node.
    def exitId_node(self, ctx:DOTParser.Id_nodeContext):
        pass


    # Enter a parse tree produced by DOTParser#string.
    def enterString(self, ctx:DOTParser.StringContext):
        pass

    # Exit a parse tree produced by DOTParser#string.
    def exitString(self, ctx:DOTParser.StringContext):
        pass


    # Enter a parse tree produced by DOTParser#interaction.
    def enterInteraction(self, ctx:DOTParser.InteractionContext):
        pass

    # Exit a parse tree produced by DOTParser#interaction.
    def exitInteraction(self, ctx:DOTParser.InteractionContext):
        pass


    # Enter a parse tree produced by DOTParser#cfsm_interaction.
    def enterCfsm_interaction(self, ctx:DOTParser.Cfsm_interactionContext):
        pass

    # Exit a parse tree produced by DOTParser#cfsm_interaction.
    def exitCfsm_interaction(self, ctx:DOTParser.Cfsm_interactionContext):
        pass


    # Enter a parse tree produced by DOTParser#choice.
    def enterChoice(self, ctx:DOTParser.ChoiceContext):
        pass

    # Exit a parse tree produced by DOTParser#choice.
    def exitChoice(self, ctx:DOTParser.ChoiceContext):
        pass


    # Enter a parse tree produced by DOTParser#fork.
    def enterFork(self, ctx:DOTParser.ForkContext):
        pass

    # Exit a parse tree produced by DOTParser#fork.
    def exitFork(self, ctx:DOTParser.ForkContext):
        pass


