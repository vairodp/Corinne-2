import os
from .DOTParser import DOTParser
"""
This file contains several functions used by check_and_fill class
and DomitillaConverter class
"""


def extract_name(path_file):
    """ Extract graph name from path """
    path_splitted = os.path.split(path_file)
    filename_splitted = path_splitted[1].split('.')
    return filename_splitted[0]


def get_string_from_tokens(ctx: DOTParser.StringContext):
    """ Given a StringContext from DOTParser,
        concatenate each character token in
        a unique string result """
    str_result = ""
    for i in ctx.getChildren():
        str_result += str(i)
    return str_result


def get_interaction_string(ctx: DOTParser.InteractionContext):
    """ Given a InteractionContext from DOTParser,
        return a 4-uple with:
        - the sender (A)
        - the receiver (B)
        - the message
        - a label string like: "A -> B : message"
    """
    # make the label
    label = str(ctx.Uppercase_letter(0)) + '->' + \
            str(ctx.Uppercase_letter(1)) + ':'
    message = ""
    for i in ctx.Lowercase_letter():
        message += str(i)
    label += message
    
    return (str(ctx.Uppercase_letter(0)), str(ctx.Uppercase_letter(1)),
            message, label)
