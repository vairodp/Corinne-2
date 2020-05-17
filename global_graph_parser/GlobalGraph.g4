/*  This file define a grammar based on Chorgram grammar
    (https://bitbucket.org/emlio_tuosto/chorgram/wiki/Home)
*/
grammar GlobalGraph;

init: g EOF | '(o)' EOF;            // (o) empty

g:  Partecipant '->' Partecipant ':' String  # interaction
    | g ';' g                       # sequential
    | g '+' g                       # choice
    | g '|' g                       # fork
    | '*' g '@' Partecipant         # loop
    | '{' g '}'                     # parenthesis
    ;
/*  NOTE: names which begin with # on the right of productions
          are not comments, but ID used by antlr4 runtime to
          build methods in the grammar listener.
*/

/*  NOTE: ANTLR allowing us to specify operator precedence.
          So, in a case without brackets , e.g. 'G + G ; G'
          ANTLR resolves the operator ambiguity in favor of the ';' operator.
          In other words, the order of productions define the binding rules for each operator,
          in this grammar ';' has priority to '+', and '+' has priority to '|'
*/

Partecipant : [A-Z]+ ;             // match lower-case & upper-case identifiers
String : [a-z]+ ;             // match lower-case & upper-case identifiers
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines, \r (Windows)