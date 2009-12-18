if __name__ == "__main__":
    import hashsimulator
    import ruleset
    rule110 = ruleset.CreateElementaryRuleSet(110)
    startingpattern = [rule110.OnState]
    backgroundpattern = [rule110.OffState]
    sim = hashsimulator.HashSimulator(rule110, startingpattern, backgroundpattern)
    atomblank = sim.GetAtomicNode(0, 0)
    atomfilled = sim.GetAtomicNode(0, 1)
    biggestfilled = atomfilled
    biggestblank = atomblank
    for x in range(0, 6):
        if x % 2 == 0:
            biggestfilled = sim.GetNode(biggestfilled, biggestblank)
        else:
            biggestfilled = sim.GetNode(biggestblank, biggestfilled)
        biggestblank = sim.GetNode(biggestblank, biggestblank)
    
