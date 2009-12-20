class Surface:
    """
    Acts as an output from a simulator. A surface is a two dimensional
    picture of an area in the simulator. An underived surface by itself
    acts as a null device, discarding all data it recieves.
    """

    def Write(self, RuleSet, X, Y, State):
        """
        Writes data to the surface.
        """
        pass

    def Close(self):
        """
        Closes the surface and prevents more writing.
        """
        pass
