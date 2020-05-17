from fsa import FSA


class ChoreographyAutomata(FSA):
    """
        This class implement the Choreography Automata (CA).
        A CA is a Finite State Machine (FSA) where labels are in the
        form of 'A->B:m' (with A!=B) or epsilon (empty string)
    """
    
    def __init__(self, states: set, labels: set, edges: set, s0: str, participants: set):
        super().__init__(states, labels, edges, s0)
        self.participants = participants

    def __get_participants_and_message_from_label__(self, label):
        sender, receiver_message = label.split('->')
        receiver, message = receiver_message.split(':')
        return sender.strip(), receiver.strip(), message.strip()
