# Generated from DOT.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DOTParser import DOTParser
else:
    from DOTParser import DOTParser

# This class defines a complete generic visitor for a parse tree produced by DOTParser.

class DOTVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DOTParser#graph.
    def visitGraph(self, ctx:DOTParser.GraphContext):
        return self.visitChildren(ctx)


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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#start_node.
    def visitStart_node(self, ctx:DOTParser.Start_nodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#start_edge.
    def visitStart_edge(self, ctx:DOTParser.Start_edgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#attr_list.
    def visitAttr_list(self, ctx:DOTParser.Attr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#id_node.
    def visitId_node(self, ctx:DOTParser.Id_nodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#string.
    def visitString(self, ctx:DOTParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#interaction.
    def visitInteraction(self, ctx:DOTParser.InteractionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#cfsm_interaction.
    def visitCfsm_interaction(self, ctx:DOTParser.Cfsm_interactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#choice.
    def visitChoice(self, ctx:DOTParser.ChoiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DOTParser#fork.
    def visitFork(self, ctx:DOTParser.ForkContext):
        return self.visitChildren(ctx)



del DOTParser