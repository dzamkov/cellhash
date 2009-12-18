def CreateElementaryRuleSet(Num = 110):
    """
    Creates a two-state cellular automata based on an input number
    between 0 and 255. Numbers such as 30,110,126,150
    and 182 produce intresting automata.
    """
    Num = Num % 256
    class ElementaryRuleSet:
        RuleTable = None
        """
        Table of rules in the form {(left, center, right) : newstate}
        """

        OnState = 1
        """
        State that indicates a cell that is on.
        """

        OffState = 0
        """
        State that indicates a cell is off.
        """
        
        def __init__(self, Num):
            # Create RuleSet
            self.RuleTable = { }
            cnum = Num
            bnum = 1
            for l in range(0, 2):
                for c in range(0, 2):
                    for r in range(0, 2):
                        key = (l, c, r)
                        if cnum % (bnum * 2) > 0:
                            cnum = cnum - bnum
                            self.RuleTable[key] = self.OnState
                        else:
                            self.RuleTable[key] = self.OffState
                        bnum = bnum * 2
            pass

        def Next(self, Left, Center, Right):
            # Get next state from table
            return self.RuleTable[(Left, Center, Right)]

        def Print(self, State):
            # Gets char representation of state
            if State == self.OnState:
                return "*"
            else:
                return " "
    rset = ElementaryRuleSet(Num)
    return rset
