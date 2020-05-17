/*
    This file defines a grammar to recognize graphs
    in DOT language. But it's higly customized for
    our purpose: recognize a Choreography Automaton (CAs).
*/
grammar DOT;

/* So a graph in our grammar start with a 'digraph' string,
   followed by a name, and a block with statement like this:
   
        digraph MyGraphName {
            statement1
            statement2
            ...
        }
    NOTE: '\n' (newlines) are required at start of block
          after '{' and at the end of each statement.
 */

graph   :   'digraph' string '{' '\n' stmt_list+ '}' ;

stmt_list:  stmt '\n' ;

/* A statement could be:
    - x1 [... some attributes ...]       // a node
	- x1 -> x2                           // a simply edge (no label)
    - x1 -> x2 [label="..."]             // a label edge

   where x1 and x2 are IDs of nodes (a number or a couple of numbers).
*/
stmt : node | edge | start_node | start_edge ;

node : id_node '[' (attr_list ','?)* ']' ;

edge : id_node '->' id_node ('[' 'label' '=' '"' label? '"' ']')? ;

/*  These are two special cases to specific a start node.
    So, create a normal node with 's0' name as ID and with
    an empty label.  */
start_node : 's0' '[' 'label' '=' '"' '"' (','? attr_list)* ']' ;
/*  Therefore, create an edge from this node to the initial
    point you want to specify. */
start_edge : 's0' '->' ('"' string '"' | Number) ;

attr_list  : 'label' '=' '"' label? '"'
           | 'shape' '=' Shape
           /* height and width are meaningful to hide
              the node s0 and view just the arrow
              enter in the start node. */
           | 'height' '=' ('"' string '"' | Number)
           | 'width' '=' ('"' string '"' | Number)
           ;

id_node : Number | '"' string '"' ;

string : (Uppercase_letter | Lowercase_letter | Number | '-' | '_' | ',')+ ;

/* In Choreography automaton we have a set of labels like:

    " A -> B : some_msg "
    
   So we check (at syntactic analysis time) if the input entered
   respect this format, otherwise we reject it.
*/

label :  Uppercase_letter '->' Uppercase_letter ':' (Lowercase_letter)+ # interaction
      |  Uppercase_letter Uppercase_letter ('?'|'!') (Lowercase_letter)+ # cfsm_interaction

            /* these tokens are specified to recognize also
               graphs from Domitilla's Graphs format
               (https://github.com/dedo94/Domitilla.git) */
      | '+' # choice
      | '|' # fork  /* NOTE: we reject Fork nodes */
      ;

Shape : 'circle' | 'square' | 'diamond' | 'rect' | 'doublecircle' | 'none' ;

Uppercase_letter : [A-Z];
Lowercase_letter : [a-z];
Number : [0-9]+;
WS: [ \t]+ -> skip;   // skip spaces and tabs