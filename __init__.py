if __name__ == "__main__":
    import hashsimulator
    import ruleset
    import textsurface
    import sys
    rnum = int(input("rule number : "))
    spat = input("starting pattern : ")
    bpat = input("background pattern : ")
    size = int(input("size : "))
    offset = int(input("offset : "))
    output = input("output file : ")
    rule = ruleset.CreateElementaryRuleSet(rnum)
    startingpattern = []
    backgroundpattern = []
    for c in spat:
        if c == "0":
            startingpattern.append(0)
        else:
            startingpattern.append(1)
    for c in bpat:
        if c == "0":
            backgroundpattern.append(0)
        else:
            backgroundpattern.append(1)
    sim = hashsimulator.HashSimulator(rule, startingpattern, backgroundpattern)
    t = textsurface.TextSurface(size, size)
    sim.Write(offset, 0, size, size, t)
    t.Close()
    t.OutputFile(output)
    sim.PrintStatus()
    
