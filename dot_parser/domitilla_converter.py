from antlr4 import *
from .DOTLexer import DOTLexer
from .DOTParser import DOTParser
from .MyErrorListener import MyErrorListener
from .domitilla_visitor import DomitillaVisitor


def domitilla_converter(ca, path_file, path_store):
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
    result = DomitillaVisitor(ca, path_file, path_store).visit(tree)
    # result contains a 3-tuple with the updated ca,
    # a new path for the converted graph and the
    # graph name
    
    ca = result[0]
    message = "[CONVERTED] " + result[1]
    return ca, message
