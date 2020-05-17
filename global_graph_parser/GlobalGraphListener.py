# Generated from GlobalGraph.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GlobalGraphParser import GlobalGraphParser
else:
    from GlobalGraphParser import GlobalGraphParser

# This class defines a complete listener for a parse tree produced by GlobalGraphParser.
class GlobalGraphListener(ParseTreeListener):

    # Enter a parse tree produced by GlobalGraphParser#init.
    def enterInit(self, ctx:GlobalGraphParser.InitContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#init.
    def exitInit(self, ctx:GlobalGraphParser.InitContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#fork.
    def enterFork(self, ctx:GlobalGraphParser.ForkContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#fork.
    def exitFork(self, ctx:GlobalGraphParser.ForkContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#loop.
    def enterLoop(self, ctx:GlobalGraphParser.LoopContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#loop.
    def exitLoop(self, ctx:GlobalGraphParser.LoopContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#sequential.
    def enterSequential(self, ctx:GlobalGraphParser.SequentialContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#sequential.
    def exitSequential(self, ctx:GlobalGraphParser.SequentialContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#interaction.
    def enterInteraction(self, ctx:GlobalGraphParser.InteractionContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#interaction.
    def exitInteraction(self, ctx:GlobalGraphParser.InteractionContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#choice.
    def enterChoice(self, ctx:GlobalGraphParser.ChoiceContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#choice.
    def exitChoice(self, ctx:GlobalGraphParser.ChoiceContext):
        pass


    # Enter a parse tree produced by GlobalGraphParser#parenthesis.
    def enterParenthesis(self, ctx:GlobalGraphParser.ParenthesisContext):
        pass

    # Exit a parse tree produced by GlobalGraphParser#parenthesis.
    def exitParenthesis(self, ctx:GlobalGraphParser.ParenthesisContext):
        pass


