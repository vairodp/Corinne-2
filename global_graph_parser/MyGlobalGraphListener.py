from chor_auto import ChoreographyAutomata
from graphviz import Digraph
from .GlobalGraphListener import GlobalGraphListener



class ForkStatementDetected(Exception):
    def __init__(self):
        self.message = ["[WARNING] Fork founded!",
                        "I can't accept that"]


class MyGlobalGraphListener(GlobalGraphListener):
    """
    There are 2 methods (enter and exit) for each rule of the grammar.
    As the walker encounters the node for rule Choice, for example,
    it triggers enterChoice(). After the walker visits all children
    of the Choice node, it triggers exitChoice().

    NOTE: For our purpose, we can't do anything in enter methods
    (except for the enterInit). We need to go down in parse tree
    and store information in stack, before we'll be able to build
    the graph.
    """
    
    def __init__(self, graph_name, path_store):
        self.path_store = path_store
        self.stack = []
        self.states = set()
        self.labels = set()
        self.edges = set()
        self.participants = set()
        self.g = Digraph(graph_name)  # initializes graph
        self.count = 0  # needed to number each node
    
    def __get_participants_and_message_from_label__(self, label):
        sender, receiver_message = label.split('->')
        receiver, message = receiver_message.split(':')
        return sender.strip(), receiver.strip(), message.strip()
    
    # Enter a parse tree produced by GlobalGraph#Init.
    def enterInit(self, ctx):
        self.count += 1
    
    # Exit a parse tree produced by GlobalGraph#Init.
    def exitInit(self, ctx):
        node = self.stack.pop()
        self.g.node('s0', label="", shape='none', height='0', width='0')
        self.g.edge('s0', "0")
        self.edges.add(("0", "", str(node[1]), "", "", ""))
        #self.g.edge("0", str(node[1]))
        self.edges.add((str(node[2]), "", str(self.count), "", "", ""))
        #self.g.edge(str(node[2]), str(self.count))
        for edge in self.edges:
            self.states.add(edge[0])
            self.states.add(edge[2])
        ca = ChoreographyAutomata(self.states, self.labels,
                                  self.edges, '0',
                                  self.participants)
        ca.delete_epsilon_moves()
        for edge in ca.edges:
            self.g.edge(str(edge[0]), str(edge[2]), label=edge[1])
        
        self.g.save(self.path_store)  # draw the graph
    
    # Enter a parse tree produced by GlobalGraph#interaction.
    def enterInteraction(self, ctx):
        pass
    
    # Exit a parse tree produced by GlobalGraph#interaction.
    def exitInteraction(self, ctx):
        node = ['interaction', self.count, self.count + 1]
        self.stack.append(node)
        self.count += 2
        #self.g.edge(str(node[1]), str(node[2]), label=ctx.getText())
        label = ctx.getText()
        sender, receiver, message = self.__get_participants_and_message_from_label__(label)
        self.participants.add(sender)
        self.participants.add(receiver)
        self.labels.add(label)
        self.edges.add((str(node[1]), label, str(node[2]), sender, receiver, message))

    # Enter a parse tree produced by GlobalGraph#sequential.
    def enterSequential(self, ctx):
        pass
    
    # Exit a parse tree produced by GlobalGraph#sequential.
    def exitSequential(self, ctx):
        right = self.stack.pop()
        left = self.stack.pop()
        node = ['sequential', left[1], right[2]]
        self.stack.append(node)
        #self.g.edge(str(left[2]), str(right[1]))
        self.edges.add((str(left[2]), "", str(right[1]), "", "", ""))
    
    # Enter a parse tree produced by GlobalGraph#choice.
    def enterChoice(self, ctx):
        pass
    
    # Exit a parse tree produced by GlobalGraph#choice.
    def exitChoice(self, ctx):
        right = self.stack.pop()
        left = self.stack.pop()
        if left[0] == 'choice':
            node = ['choice', left[1], left[2]]
            self.stack.append(node)
            #self.g.edge(str(left[1]), str(right[1]))
            self.edges.add((str(left[1]), "", str(right[1]), "", "", ""))
            #self.g.edge(str(right[2]), str(left[2]))
            self.edges.add((str(right[2]), "", str(left[2]), "", "", ""))
        else:
            choice_node_start = str(self.count)
            self.count += 1
            choice_node_end = str(self.count)
            self.count += 1
            node = ['choice', choice_node_start, choice_node_end]
            self.stack.append(node)
            #self.g.edge(choice_node_start, str(left[1]))
            self.edges.add((choice_node_start, "", str(left[1]), "", "", ""))
            #self.g.edge(choice_node_start, str(right[1]))
            self.edges.add((choice_node_start, "", str(right[1]), "", "", ""))
            #self.g.edge(str(left[2]), choice_node_end)
            self.edges.add((str(left[2]), "", choice_node_end, "", "", ""))
            #self.g.edge(str(right[2]), choice_node_end)
            self.edges.add((str(right[2]), "", choice_node_end, "", "", ""))
    
    # Enter a parse tree produced by GlobalGraph#fork.
    def enterFork(self, ctx):
        raise ForkStatementDetected
    
    # Exit a parse tree produced by GlobalGraph#fork.
    def exitFork(self, ctx):
        raise ForkStatementDetected
    
    # Enter a parse tree produced by GlobalGraph#loop.
    def enterLoop(self, ctx):
        pass
    
    # Exit a parse tree produced by GlobalGraph#loop.
    def exitLoop(self, ctx):
        node_to_loop = self.stack.pop()
        loop_node_start = str(self.count)
        self.count += 1
        loop_node_end = str(self.count)
        self.count += 1
        node = ['loop', loop_node_start, loop_node_end]
        self.stack.append(node)
        #self.g.edge(loop_node_start, str(node_to_loop[1]))
        self.edges.add((loop_node_start, "", str(node_to_loop[1]), "", "", ""))
        #self.g.edge(str(node_to_loop[2]), loop_node_end)
        self.edges.add((str(node_to_loop[2]), "", loop_node_end, "", "", ""))
        #self.g.edge(loop_node_end, loop_node_start)
        self.edges.add((loop_node_end, "", loop_node_start, "", "", ""))
    # Enter a parse tree produced by GlobalGraph#parenthesis.
    def enterParenthesis(self, ctx):
        pass
    
    # Exit a parse tree produced by GlobalGraph#parenthesis.
    def exitParenthesis(self, ctx):
        pass
