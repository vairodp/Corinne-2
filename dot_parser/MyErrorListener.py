from antlr4.error.ErrorListener import ErrorListener


class parseError(Exception):

    def __init__(self, message):
        self.message = message

class MyErrorListener(ErrorListener):
    '''
    MyErrorListener redirect Errors from stdout
    (normal behaviour of DefaultErrorListener)
    to an exception
    '''

    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        position_of_the_error = "InputError in [line: " + str(line) + ",column: " + str(column) + "]"
        error = [position_of_the_error, msg]
    
        raise parseError(error)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("reportAmbiguity")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("reportAttemptingFullContext")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("reportContextSensitivity")