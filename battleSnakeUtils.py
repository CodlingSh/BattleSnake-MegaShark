def drawHumanReadableArena(arena: list):
    """
        arena: a 2D list containing info about every square in the arena

        returns a multi line string representation of the arena in an easier to read format.
    """
    
    for y in reversed(arena):
        for x in y:
            print(str(x) + " ", end="")
        print("")
