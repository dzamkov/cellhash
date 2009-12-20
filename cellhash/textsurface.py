import surface

class TextSurface(surface.Surface):
    """
    Surface that outputs a cellular automata simulation
    as multiline text.
    """

    __Data = None
    """
    List of characters making up the surface.
    """

    __Size = (0, 0)
    """
    Size of the text surface.
    """

    def __init__(self, Width, Height):
        self.__Size = (Width, Height)
        self.__Data = [' ' for x in range(0, Width * Height)]

    def Write(self, RuleSet, X, Y, State):
        self.__Data[X + (Y * self.__Size[0])] = RuleSet.Print(State)

    def Close(self):
        pass

    def OutputFile(self, FileName = "output.txt"):
        """
        Outputs to the file of the specified name.
        """
        file = open(FileName, 'w')
        self.Output(file)
        file.close()

    def Output(self, Stream):
        """
        Outputs to a stream.
        """
        for y in range(0, self.__Size[1]):
            string = ''
            for x in range(0, self.__Size[0]):
                string = string + self.__Data[x + (y * self.__Size[0])]
            string = string + '\n'
            Stream.write(string)
        pass
