class HashNode:
    """
    Node in the cellular automata simulator.
    """

    A = None
    """
    Left starting point of the node.
    """

    B = None
    """
    Right starting point of the node.
    """

    Result = None
    """
    Result of the computations of a and b.
    """

    Level = 0
    """
    Level of the node. The size of the node in states
    is 2^Level. The size of the result is half that.
    """

    def Compute(self, Simulator):
        """
        Computes the result of the node.
        """
        pass

    def GetResult(self, Simulator):
        """
        Gets the result of the node.
        """
        if self.Result == None:
            self.Compute(Simulator)
        return self.Result

    def Print(self, Simulator):
        """
        Prints the char representation of a and b.
        """
        return self.A.Print(Simulator) + self.B.Print(Simulator)

class AtomicHashNode(HashNode):
    """
    Small hash node with no result. Always at level 1.
    Combination of two states.
    """
    
    def __init__(self, A, B):
        HashNode.__init__(self)
        self.A = A
        self.B = B
        self.Level = 1

    def Compute(self, Simulator):
        pass

    def Print(self, Simulator):
        rset = Simulator.RuleSet
        return rset.Print(self.A) + rset.Print(self.B)

class SimpleHashNode(HashNode):
    """
    Slightly larger hash node that is the combination of two
    atomic nodes. Always at level 2.
    """

    def __init__(self, A, B):
        HashNode.__init__(self)
        self.A = A
        self.B = B
        self.Level = 2

    def Compute(self, Simulator):
        rset = Simulator.RuleSet
        na = rset.Next(self.A.A, self.A.B, self.B.A)
        nb = rset.Next(self.A.B, self.B.A, self.B.B)
        self.Result = Simulator.GetAtomicNode(na, nb)

class CompoundHashNode(HashNode):
    """
    Combination of two smaller nodes. Can have any level greater than
    2.
    """

    def __init__(self, A, B):
        HashNode.__init__(self)
        self.A = A
        self.B = B
        self.Level = A.Level + 1

    def Compute(self, Simulator):
        center = Simulator.GetNode(self.A.B, self.B.A)
        resa = self.A.GetResult(Simulator)
        resb = self.B.GetResult(Simulator)
        rescenter = center.GetResult(Simulator)
        na = Simulator.GetNode(resa, rescenter)
        nb = Simulator.GetNode(rescenter, resb)
        resna = na.GetResult(Simulator)
        resnb = nb.GetResult(Simulator)
        self.Result = Simulator.GetNode(resna, resnb)

class HashSimulator:
    """
    Cellular automata simulator using hashing.
    """

    RuleSet = None
    """
    The ruleset used by the simulator.
    """

    Nodes = None
    """
    A dict of a dict of nodes in the form {Level : {(A, B) : Node}}
    """

    def __init__(self, RuleSet, StartingPattern, BackgroundPattern):
        """
        Creates a new simulator with a ruleset, a starting pattern
        and a background pattern. The patterns are given as lists
        of states. For now, the background pattern must have a length
        of 1.
        """
        self.RuleSet = RuleSet
        self.Nodes = { }

    def GetNode(self, A, B):
        """
        Gets the node that is the combination of a and b.
        """
        level = A.Level + 1
        try:
            return self.Nodes[level][A, B]
        except(KeyError):
            if level == 2:
                sn = SimpleHashNode(A, B)
                self.__Level(level)[A, B] = sn
                return sn
            else:
                cn = CompoundHashNode(A, B)
                self.__Level(level)[A, B] = cn
                return cn

    def GetAtomicNode(self, A, B):
        """
        Gets an atomic hash node that is the combination of the two supplied
        states.
        """
        try:
            return self.Nodes[1][A, B]
        except(KeyError):
            ap = AtomicHashNode(A, B)
            self.__Level(1)[A, B] = ap
            return ap

    def __Level(self, Level):
        """
        Returns a level safelty.
        """
        try:
            return self.Nodes[Level]
        except:
            l = dict()
            self.Nodes[Level] = l
            return l

    def PrintStatus(self):
        """
        Gives a status report.
        """
        computed = 0
        uncomputed = 0
        atomic = 0
        for x in self.Nodes.values():
            for y in x.values():
                if y.Result != None:
                    computed = computed + 1
                else:
                    uncomputed = uncomputed + 1
                if y.Level == 1:
                    atomic = atomic + 1
        print("Computed Nodes: " + str(computed))
        print("Uncomputed Nodes: " + str(uncomputed))
        print("Atomic Nodes: " + str(atomic))
        print("Total Nodes: " + str(computed + uncomputed))
