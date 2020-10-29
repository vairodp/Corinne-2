import os, itertools

#TODO inserire introduzione


# Check wathever a run has cycle
# with at most one occurrence

def check_q_branch(array):

        for i in array:
            if array.count(i) == 3:
                return False

        return True

# DFS given a set of transitions

def search(i, arr, insieme1, runs):

    if (i == None):
        for j in insieme1:
            arr = [j[0],j[2]]
            runs.append(arr)
            search(j[2], arr, insieme1, runs)
    else:
        for j in insieme1:
            if i == j[0]:
                io = []
                for ite in arr:
                    io.append(ite)
                io.append(j[2])
                if check_q_branch(io):
                    runs.append(io)
                    search(j[2], io, insieme1, runs)

# Given a set of transitions, it
# returns all possible
# pre-candidate q-branches

def get_all_runs(set):

    runs = []
    search(None, None, set, runs)

    return runs

# Given two states, returns the
# transition betweeen those two
# states

def returnedge(s1, s2, edges):
    for e in edges:
        if e[0] == s1 and e[2] == s2:
            return e

# Support function of 
# "get_candidate_runs"
# Iters every passed 
# run and checks
# sublist()

def iter(a, runs):

    for b in runs:
        if sublist(a, b):
            return True
    return False

# Given a set of runs, filters the
# maximal pre-candiddate q-branch
# (candidate q-branch)

def get_candidate_runs(runs, states):

    candidates = []

    for a in runs:
        
        if iter(a, runs) == False:
            candidates.append(a)

    return candidates

# Returns True if the path is a
# pre-candididate q-branch

def sublist(a, b):

    if len(a) <= len(b) and a != b:

        for i in range(len(a)):
            if a[i] != b[i]:
                return False

        return True

    return False

# Check whatever a pair of runs  is cofinal, with no commons node but the first and the last one

def first_qspan_condition(sigma1, sigma2):

    alpha = sigma1.copy()
    beta = sigma2.copy()

    if alpha[0] == beta[0] and alpha[-1] == beta[-1]:

        a = alpha.pop(0)
        beta.pop(0)
        b = alpha.pop(-1)
        beta.pop(-1)


        if not (any(x in alpha for x in beta)) and a not in alpha and b not in alpha and a not in beta and b not in beta :
            return True
    return False

# Check whatever a pair of runs is two candidate
# q-branches with no common node but the first

def second_qspan_condition(sigma1, sigma2, candidates):

    a = sigma1.copy()
    b = sigma2.copy()

    if (sigma1 in candidates) and (sigma2 in candidates):
        a.pop(0)
        b.pop(0)

        if not (any(x in a for x in b)):
            return True
        return False
    return False

# Check whatever a pair is formed by a candidate
# q-branch and a loop on q with no other common 
# nodes 

def third_qspan_condition(sigma1, sigma2, candidates):

    a = sigma1.copy()
    b = sigma2.copy()

    # First loop
    if a[0] == a[-1]:


        if b in candidates:
            a.pop(0)
            a.pop(-1)

            if not (any(x in a for x in b)):
                return True

    # Second loop
    if b[0] == b[-1]:

        if a in candidates:
            b.pop(0)
            b.pop(-1)

            if not (any(y in b for y in a)):
                return True

    return False


# Well-branchedness first condition:
# Check if in all edges if a state is sender it cannot also be receiver in the same edge

def well_branchedness_first_condition(edges, states):

    for i in states:
        senders = []
        receivers = []

        for j in edges:
            if j[0] == i:
                senders.append(j[3])
                receivers.append(j[4])

                if j[4] in senders:

                   return ("participant "+str(j[4]+" is a sender and also a receiver in transitions from "+j[0]))

                if j[3] in receivers:

                    return ("participant "+str(j[3]+" is a sender and also a receiver in transitions from "+j[0]))

    return None

# Well-branchedness secondd condition:
# Check for each edge where a state is not a sender in each transition if this two edges
# are concurrent

def well_branchedness_second_condition(edges, states, participants):

    for s in states:
        for a in participants:

            for i in edges:
                if i[3] == a:
                    for j in edges:
                        if i[0] == j[0] and i[3] != j[3]:


                            for x in edges:
                                for y in edges:

                                    if x[0] == i[2] and y[0] == j[2]:
                                        # Found all edges

                                        if x[2] == y[2] and x[1] == j[1] and y[1] == i[1]:
                                            return None

                            return (str(i[0]+"  |"+str(i[1])+"|  "+str(i[2])+"  |"+str(j[1])+"|  "+str(j[2])))
    return None


# Given a set of transition and a partecipant, returns
# the first label where the partecipant appear
def get_first(participant, edges):
    if edges != None:
        for run in edges:
            if participant == run[3] or participant == run[4]:
                return run
    return None

# Given a partecipant and two sets of transition 
# it returns the first not different label where
# the partecipant appears
def get_first_label(participant, edges1, edges2):

    firstlabel = get_first(participant, edges1)
    secondlabel = get_first(participant, edges2)

    if (firstlabel != None and secondlabel != None):
        if firstlabel[1] == secondlabel[1]:
            edges1.remove(firstlabel)
            edges2.remove(secondlabel)

            return (get_first_label(participant, edges1, edges2))

        else:
            return firstlabel,secondlabel

    else:
        return firstlabel, secondlabel


# Simply check the "form" of the couple in the last part of the
# third Well-Brandhedness condition

def check_form(edge1, edge2, B):

    C = edge1[3]
    D = edge2[3]
    m = edge1[5]
    n = edge2[5]

    if ((edge1[4] == edge2[4] == B) and ((C != D) or (m != n))):

        return True

    return False

# Checks if a q-span has the first pair of different labels
# on the runs on the projection of sigma1 and sigma2 given
# a partecipant checks the form in "check_form"

def check_validity(sigma1, sigma2, edges, participants):

    edges1 = []
    edges2 = []

    for i in range(len(sigma1)):

        if i+1 >= len(sigma1):
            break

        edges1.append(returnedge(sigma1[i], sigma1[i+1], edges))

    for i in range(len(sigma2)):

        if i+1 >= len(sigma2):
            break

        edges2.append(returnedge(sigma2[i], sigma2[i+1], edges))

    B = participants.copy()

    chooser = returnedge(sigma1[0], sigma2[1], edges)

    A = chooser[3]
    B.remove(A)

    for bee in B:

        firstlabel,secondlabel = get_first_label(bee, edges1, edges2)
        
        if (firstlabel == None) or (secondlabel == None):
            if firstlabel != secondlabel:
                return bee

        elif firstlabel[1] != secondlabel[1]:

            if not (check_form(firstlabel, secondlabel, bee)):
                return bee

    return None

# Well-branchedness third condition:
# First it finds every q-span where A chooses at, then it checks for every q-span if they pass the validity check in the definition
# by calling "check_validity" for every q-span

def well_branchedness_third_condition(states, edges, participants):

    runs = get_all_runs(edges)

    candidate = get_candidate_runs(runs, states)

    passed = []

    for p in states:
        
        for A in participants:

            for sigma, sigma_primo in itertools.combinations(runs, 2):

                if sigma[0] == sigma_primo[0] == p:

                    # Check if the couple is a q-span couple

                    if first_qspan_condition(sigma, sigma_primo) or second_qspan_condition(sigma, sigma_primo, candidate) or third_qspan_condition(sigma, sigma_primo, candidate):

                        # Check if they have a "chooser"

                        chooserA = returnedge(sigma[0], sigma[1], edges)
                        chooserB = returnedge(sigma_primo[0], sigma_primo[1], edges)

                        if chooserA[3] == chooserB[3] == A:
                            passed.append([sigma, sigma_primo])


    for it in range(len(passed)):

        result = check_validity(passed[it][0], passed[it][1], edges, participants)

        if not (result == None):
            return str((passed[it][0],passed[it][1], "B = ", result))

    return None

# Check edge by edge if the graph respects the first condition, if it doesn't respet it check if at that point
# at least the second condition holds

def well_sequencedness_conditions(ca):

    #first condition check for every coupple of transitions
    for i in ca.edges:
        for j in ca.edges:
            if i[2] == j[0]:
                if j[3] != i[3] and j[4] != i[4] and j[4] != i[3] and i[4] != j[3]:

                    #second condition check
                    for k in ca.edges:
                        if i[2] != k[2] and k[0] == i[0]:
                            for h in ca.edges:
                                if h[0] == k[2] and h[2] == j[0]:
                                    if  i[1] == h[1] and j[1] == k[1]:
                                        return None
                            return (str(i[0]+"  |"+str(i[1])+"|  "+str(i[2])+"  |"+str(j[1])+"|  "+str(j[2])))
                    return (str(i[0]+"  |"+str(i[1])+"|  "+str(i[2])+"  |"+str(j[1])+"|  "+str(j[2])))
    return None