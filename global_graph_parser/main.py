import sys, os
from antlr4 import *
from .GlobalGraphLexer import GlobalGraphLexer
from .GlobalGraphParser import GlobalGraphParser
from .MyGlobalGraphListener import MyGlobalGraphListener, ForkStatementDetected
from .MyErrorListener import MyErrorListener, parseError


def __extract_name__(path_file):
    path_splitted = os.path.split(path_file)
    filename_splitted = path_splitted[1].split('.')
    return filename_splitted[0]

def main(path_file, path_store):
    """
    Aim of this function is to take a string of the GlobalGraph grammar
    and translate it in a dot (graph description language) file.
    """
    graph_name = __extract_name__(path_file)

    path_store = os.path.join(path_store, graph_name + '.gv')

    input_stream = FileStream(path_file)

    # tokenizes input into word (tokens)
    lexer = GlobalGraphLexer(input_stream)
    stream = CommonTokenStream(lexer)
    # parser these tokens to recognize the sentence structure
    # and build a parse tree
    try:
        parser = GlobalGraphParser(stream)
        # remove DefaultErrorListener
        parser.removeErrorListeners()
        lexer.removeErrorListeners()
        # add MyErrorListener (See MyErrorListener.py)
        parser.addErrorListener(MyErrorListener())
        lexer.addErrorListener(MyErrorListener())
        tree = parser.init()
        # "listener" is the mechanism through we visit
        # each node of parse tree
        listener = MyGlobalGraphListener(graph_name, path_store)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
    except (parseError, ForkStatementDetected) as e:
        return e.message
    else:
        return ["Read Successfully " + str(graph_name),
               "[CREATED] " + path_store] , path_store


