if __name__ == "__main__":
    import hashsimulator
    import ruleset
    import text
    import sys
    rule110 = ruleset.CreateElementaryRuleSet(110)
    startingpattern = [1]
    backgroundpattern = [0]
    sim = hashsimulator.HashSimulator(rule110, startingpattern, backgroundpattern)

    t = text.TextSurface(70, 70)
    sim.Write(-69, 0, 70, 70, t)
    t.Output(sys.stdout)
    
