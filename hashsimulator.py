def ModularPower(Num, Pow, Mod):
    """
    Computes (Num ** Pow) % Mod really fast.
    """
    if Pow == 1:
        return Num
    else:
        if Pow % 2 == 0:
            return (ModularPower(Num, Pow // 2, Mod) ** 2) % Mod
        else:
            return (ModularPower(Num, Pow - 1, Mod) * Num) % Mod

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

    def __init__(self):
        pass

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

    def Write(self, Simulator, OffsetX, OffsetY, SizeX, SizeY, Surface):
        """
        Draws the node on a surface.
        """
        pass

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

    def Write(self, Simulator, OffsetX, OffsetY, SizeX, SizeY, Surface):
        if OffsetY < SizeY and OffsetY >= 0:
            if OffsetX < SizeX and OffsetX >= 0:
                Surface.Write(Simulator.RuleSet, OffsetX, OffsetY, self.A)
            if OffsetX + 1 < SizeX and OffsetX + 1 >= 0:
                Surface.Write(Simulator.RuleSet, OffsetX + 1, OffsetY, self.B)

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

    def Write(self, Simulator, OffsetX, OffsetY, SizeX, SizeY, Surface):
        self.A.Write(Simulator, OffsetX, OffsetY, SizeX, SizeY, Surface)
        self.B.Write(Simulator, OffsetX + 2, OffsetY, SizeX, SizeY, Surface)
        self.GetResult(Simulator).Write(Simulator, OffsetX + 1, OffsetY + 1, SizeX, SizeY, Surface)

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

    def Write(self, Simulator, OffsetX, OffsetY, SizeX, SizeY, Surface):
        height = 2 ** (self.Level - 1)
        size = height * 2
        if OffsetX < SizeX and OffsetY < SizeY and OffsetX + size >= 0 and OffsetY + height >= 0:
            center = Simulator.GetNode(self.A.B, self.B.A)
            na = Simulator.GetNode(self.A.GetResult(Simulator), center.GetResult(Simulator))
            nb = Simulator.GetNode(center.GetResult(Simulator), self.B.GetResult(Simulator))
            result = self.GetResult(Simulator)
            
            self.A.Write(
                Simulator, OffsetX, OffsetY,
                SizeX, SizeY, Surface)
            self.B.Write(
                Simulator, OffsetX + height, OffsetY,
                SizeX, SizeY, Surface)
            center.Write(
                Simulator, OffsetX + (height // 2),  OffsetY,
                SizeX, SizeY, Surface)
            na.Write(
                Simulator, OffsetX + (height // 4),  OffsetY + (height // 4),
                SizeX, SizeY, Surface)
            nb.Write(
                Simulator, OffsetX + height - (height // 4),  OffsetY + (height // 4),
                SizeX, SizeY, Surface)
            result.Write(
                Simulator, OffsetX + (height // 2), OffsetY + (height // 2),
                SizeX, SizeY, Surface)
        pass

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

    BackgroundNodes = None
    """
    The largest nodes of background at various offsets in the form: {Offset: Node}.
    Offset is the amount of cells to the right the background pattern is offset
    from the left edge of the node. Offset will never be at or larger than the
    size of the background pattern.
    """

    StartingPattern = None
    """
    List of states in the starting pattern.
    """

    BackgroundPattern = None
    """
    List of states in the background pattern.
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
        self.StartingPattern = StartingPattern
        self.BackgroundPattern = BackgroundPattern
        self.BackgroundNodes = { }

    def GetBackgroundNode(self, Level, Offset):
        """
        Gets the node of the specified level that represents the background
        at the specified offset. The offset is the distance to the right
        of the left edge of the starting pattern from which the node starts
        at. For example: if the background pattern was (1, 0, 0), the pattern
        at offset 0 will be (1, 0, 0); at -1 it will be (0, 1, 0) and at -2,
        (0, 0, 1). Background patterns are repeating so a background pattern
        of any size may be generated.
        """
        lbp = len(self.BackgroundPattern)
        soffset = Offset % lbp
        node = None
        try:
            node = self.BackgroundNodes[soffset]
            while node.Level > Level:
                node = node.A
            while node.Level < Level:
                noffset = ModularPower(2, node.Level, lbp) + soffset
                a = node
                b = self.GetBackgroundNode(node.Level, noffset)
                node = self.GetNode(a, b)
            return node
        except(KeyError):
            self.BackgroundNodes[soffset] = self.GetAtomicNode(
                self.BackgroundPattern[soffset],
                self.BackgroundPattern[(soffset + 1) % lbp])
            return self.GetBackgroundNode(Level, soffset)

    def GetStartingNode(self, Level, Offset):
        """
        Gets a starting node of the specified level and offset from
        the left edge of the starting pattern.
        """
        lsp = len(self.StartingPattern)
        lbp = len(self.BackgroundPattern)
        if Offset >= lsp:
            return self.GetBackgroundNode(Level, Offset)
        size = 2 ** Level
        if Offset + size < 0:
            return self.GetBackgroundNode(Level, Offset)
        if Level > 1:
            a = self.GetStartingNode(Level - 1, Offset)
            b = self.GetStartingNode(Level - 1, Offset + size // 2)
            return self.GetNode(a, b)
        else:
            a = None
            b = None
            if Offset >= 0:
                a = self.StartingPattern[Offset]
            else:
                a = self.BackgroundPattern[Offset % lbp]
            if Offset + 1 < lsp:
                b = self.StartingPattern[Offset + 1]
            else:
                b = self.BackgroundPattern[(Offset + 1) % lbp]
            return self.GetAtomicNode(a, b)
        pass

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
        pass

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
        pass

    def Write(self, OffsetX, OffsetY, SizeX, SizeY, Surface):
        """
        Writes data to a surface.
        """
        startingsize = SizeX * 2 + OffsetY + SizeY
        startinglevel = 1
        ss = startingsize
        while ss > 1:
            startinglevel = startinglevel + 1
            ss = ss // 2
        node = self.GetStartingNode(startinglevel, OffsetX - OffsetY - SizeY)
        node.Write(self, -OffsetY - SizeY, -OffsetY, SizeX, SizeY, Surface)

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
        pass

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
