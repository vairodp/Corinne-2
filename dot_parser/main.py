from antlr4 import *
from .DOTLexer import DOTLexer
from .DOTParser import DOTParser
from .MyErrorListener import MyErrorListener
from .MyVisitor import MyVisitor


def main(path_file):
    input_stream = FileStream(path_file)
    # tokenize input into word (tokens)
    lexer = DOTLexer(input_stream)
    stream = CommonTokenStream(lexer)
    # parser these tokens to recognize the sentence structure
    # and build a parse tree
    parser = DOTParser(stream)
    # remove DefaultErrorListener
    parser.removeErrorListeners()
    lexer.removeErrorListeners()
    # add MyErrorListener (See MyErrorListener.py)
    parser.addErrorListener(MyErrorListener())
    lexer.addErrorListener(MyErrorListener())
    
    tree = parser.graph()
    # result is a 3-tuple contains the choreography automaton
    # of the input graph, a boolean_value to verify if a Domitilla
    # graph was inserted, and the graph name
    return MyVisitor().visit(tree)

