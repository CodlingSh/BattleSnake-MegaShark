import random
import battleSnakeUtils

def getInfo() -> dict:
    """
    This function controls the appearance of MegaShark
    """
    return {
        "apiversion": "1",
        "author": "codlinsh",
        "color": "#a79d9d",
        "head": "shark",  
        "tail": "do-sammy"
    }

def chooseMove(data: dict):
    """
    data: Dictionary of all of the data of the game board. Such as snake positions, arena size, and food positions
  
    return: A String with the move to make. Can either be "up", "down", "left", "right"
    """
    
    # moves info
    possibleMoves = ["up", "down", "left", "right"]

    # Arena info
    arenaDimensions = {"width": data["board"]["width"], "height": data["board"]["height"]}
    arenaOverview = [] # A representation of the state of the arena as a 2D array
  
    # Snake info
    mySnake = data["you"] # A dictionary with info about my snake
    enemySnakes = data["board"]["snakes"] # A dictionary with info about enemy snakes
    foodLocations = data["board"]["food"] # A dictionary with the coordinates for food
  
    arenaOverview = drawArena(arenaDimensions, mySnake, enemySnakes, foodLocations, data["turn"])

    # Function calls to narrow down the list of possible moves
    possibleMoves = avoidWalls(arenaDimensions, mySnake, possibleMoves)
    possibleMoves = avoidDeath(arenaOverview, mySnake, possibleMoves)

    # Make arena easier to read in terminal
    battleSnakeUtils.drawHumanReadableArena(arenaOverview)
    #for row in arenaOverview:
    #    print(row)
    
    print("Possible Moves: " + str(possibleMoves))
    return random.choice(possibleMoves)

def drawArena(dimensions: dict, megaShark: dict, snakes: dict, food: dict, turn: int):
    """
    """

    # Empty list to store the data for the arena
    arena = []

    # Draw base arena with nothing in it
    for y in range(dimensions["height"]):
        arena.append([0] * dimensions["width"])

    # Add food
    for pos in food:
        arena[pos["y"]][pos["x"]] = 2

    # Add enemies
    for snake in snakes:
        if snake["id"] != megaShark["id"]:
            for pos in snake["body"]:
                arena[pos["y"]][pos["x"]] = 3
            arena[snake["head"]["y"]][snake["head"]["x"]] = "H"
            if snake["head"] not in food:
                arena[snake["body"][-1]["y"]][snake["body"][-1]["x"]] = "T"

    # Add MegaShark
    for pos in megaShark["body"]:
        arena[pos["y"]][pos["x"]] = 1
    arena[megaShark["head"]["y"]][megaShark["head"]["x"]] = "M"
    if megaShark["head"] not in food and turn > 2:
        arena[megaShark["body"][-1]["y"]][megaShark["body"][-1]["x"]] = "T"

    #print(megaShark["body"][-1]["x"])



    # Reverse the list to match the way BattleSnake displays the list
    #arena.reverse()

    return arena

def avoidWalls(dimensions: dict, megaShark: dict, possibleMoves: list):
    """
    """

    # Check if MegaShark is on the far left of map
    if megaShark["head"]["x"] == 0:
        possibleMoves.remove("left")
    # Check if MegaShark is on the far right of map
    if megaShark["head"]["x"] == dimensions["width"] - 1:
        possibleMoves.remove("right")
    # Check if MegaShark is on the bottom of map
    if megaShark["head"]["y"] == 0:
        possibleMoves.remove("down")
    # Check if MegaShark is on the top of map
    if megaShark["head"]["y"] == dimensions["height"] -1:
        possibleMoves.remove("up")

    return possibleMoves

def avoidDeath(arena: list, megaShark: dict, possibleMoves: list):
    """
    """


    goodSpots = [0, 2, "T"]
    
    # Check if an obstacle is 1 space up from MegaShark
    if "up" in possibleMoves:
        if arena[megaShark["head"]["y"] + 1][megaShark["head"]["x"]] not in goodSpots:
            possibleMoves.remove("up")
    # Check if an obstacle is 1 space down from MegaShark
    if "down" in possibleMoves:
        if arena[megaShark["head"]["y"] - 1][megaShark["head"]["x"]] not in goodSpots:
            possibleMoves.remove("down")
    # Check if an obstacle is 1 space left from MegaShark
    if "left" in possibleMoves:
        if arena[megaShark["head"]["y"]][megaShark["head"]["x"] - 1] not in goodSpots:
            possibleMoves.remove("left")
    # Check if an obstacle is 1 space right from MegaShark
    if "right" in possibleMoves:
        if arena[megaShark["head"]["y"]][megaShark["head"]["x"] + 1] not in goodSpots:
            possibleMoves.remove("right")

    return possibleMoves

#def floodFill(sx: int, sy: int):












