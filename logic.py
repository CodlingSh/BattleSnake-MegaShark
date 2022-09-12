import random
import copy
from math import sqrt
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
    prefferedMoves = []
    possibleMoves = ["up", "down", "left", "right"]

    # Arena info
    arenaDimensions = {"width": data["board"]["width"], "height": data["board"]["height"]}
    arenaHazards = data["board"]["hazards"]
    arenaOverview = [] # A representation of the state of the arena as a 2D array
  
    # Snake info
    mySnake = data["you"] # A dictionary with info about my snake
    enemySnakes = data["board"]["snakes"] # A dictionary with info about enemy snakes
    foodLocations = data["board"]["food"] # A dictionary with the coordinates for food

    # Variables to help determine best possible path
    upMoves = 0
    downMoves = 0
    leftMoves = 0
    rightMoves = 0
    mostMoves = 0
  
    arenaOverview = drawArena(arenaDimensions, mySnake, enemySnakes, foodLocations, arenaHazards, data["turn"])

    # Function calls to narrow down the list of possible moves
    possibleMoves = avoidWalls(arenaDimensions, mySnake, possibleMoves)
    possibleMoves = avoidDeath(arenaOverview, mySnake, possibleMoves)

    if "up" in possibleMoves:
        upMoves = countPath(floodFill(copy.deepcopy(arenaOverview), mySnake["head"]["x"], mySnake["head"]["y"] + 1))
    if "down" in possibleMoves:
        downMoves = countPath(floodFill(copy.deepcopy(arenaOverview), mySnake["head"]["x"], mySnake["head"]["y"] - 1))
    if "left" in possibleMoves:
        leftMoves = countPath(floodFill(copy.deepcopy(arenaOverview), mySnake["head"]["x"] - 1, mySnake["head"]["y"]))
    if "right" in possibleMoves:
        rightMoves = countPath(floodFill(copy.deepcopy(arenaOverview), mySnake["head"]["x"] + 1, mySnake["head"]["y"]))

    # Check which direction will lead to the most moves
    mostMoves = max([upMoves, downMoves, leftMoves, rightMoves])

    if "up" in possibleMoves:
        if upMoves != mostMoves:
            possibleMoves.remove("up")
    if "down" in possibleMoves:
        if downMoves != mostMoves:
            possibleMoves.remove("down")
    if "left" in possibleMoves:
        if leftMoves != mostMoves:
            possibleMoves.remove("left")
    if "right" in possibleMoves:
        if rightMoves != mostMoves:
            possibleMoves.remove("right")

    # print(upMoves)
    # print(downMoves)
    # print(leftMoves)
    # print(rightMoves)

    if len(foodLocations) != 0:
        prefferedMoves = chaseClosestFood(mySnake["head"], foodLocations, prefferedMoves)
        random.shuffle(prefferedMoves)

    battleSnakeUtils.drawHumanReadableArena(arenaOverview)
    print("Preffered Moves: " + str(prefferedMoves))
    print("Possible Moves: " + str(possibleMoves))

    for move in prefferedMoves:
        if move in possibleMoves:
            return move


    return random.choice(possibleMoves)

def drawArena(dimensions: dict, megaShark: dict, snakes: dict, food: dict, hazards: dict, turn: int):
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
            # Check if MegaShark will survive a head on collision
            if snake["length"] >= megaShark["length"]:
                arena[snake["head"]["y"] + 1][snake["head"]["x"]] = "h"
                arena[snake["head"]["y"] - 1][snake["head"]["x"]] = "h"
                arena[snake["head"]["y"]][snake["head"]["x"] + 1] = "h"
                arena[snake["head"]["y"]][snake["head"]["x"] - 1] = "h"
            for pos in snake["body"]:
                arena[pos["y"]][pos["x"]] = 3
            arena[snake["head"]["y"]][snake["head"]["x"]] = "H"
            if snake["head"] not in food:
                arena[snake["body"][-1]["y"]][snake["body"][-1]["x"]] = "T"

    # Add MegaShark
    for pos in megaShark["body"]:
        arena[pos["y"]][pos["x"]] = 1
    arena[megaShark["head"]["y"]][megaShark["head"]["x"]] = "M"
    if megaShark["head"] not in food and turn > 3 and megaShark["length"] >= 4:
        arena[megaShark["body"][-1]["y"]][megaShark["body"][-1]["x"]] = "T"

    # Add hazard
    for hazard in hazards:
        arena[hazard["y"]][hazard["x"]] = "Z"
    #print(megaShark["body"][-1]["x"])

    # Reverse the list to match the way BattleSnake displays the list
    #arena.reverse()

    return arena

def avoidWalls(dimensions: dict, megaShark: dict, possibleMoves: list):
    """
    """
    print("head Y: " + str(megaShark["head"]["y"]))
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

    # Check if an obstacle is 1 space up from MegaShark
    if "up" in possibleMoves:
        if arena[megaShark["head"]["y"] + 1][megaShark["head"]["x"]] not in [0, 2, "T"]:
            possibleMoves.remove("up")
    # Check if an obstacle is 1 space down from MegaShark
    if "down" in possibleMoves:
        if arena[megaShark["head"]["y"] - 1][megaShark["head"]["x"]] not in [0, 2, "T"]:
            possibleMoves.remove("down")
    # Check if an obstacle is 1 space left from MegaShark
    if "left" in possibleMoves:
        if arena[megaShark["head"]["y"]][megaShark["head"]["x"] - 1] not in [0, 2, "T"]:
            possibleMoves.remove("left")
    # Check if an obstacle is 1 space right from MegaShark
    if "right" in possibleMoves:
        if arena[megaShark["head"]["y"]][megaShark["head"]["x"] + 1] not in [0, 2, "T"]:
            possibleMoves.remove("right")

    return possibleMoves

def floodFill(arena: list, sx: int, sy: int):
    """
    """    

    if arena[sy][sx] in [0, 2, "T"]:
        arena[sy][sx] = 6

        # Check up
        if sy < len(arena) - 1:
            floodFill(arena, sx, sy + 1)
        # Check Down
        if sy > 0:
            floodFill(arena, sx, sy - 1)
        # Check Left
        if sx > 0:
            floodFill(arena, sx - 1, sy)
        # Check Right
        if sx < len(arena[sy]) - 1:
            floodFill(arena, sx + 1, sy)

    return arena

def countPath(arena: list):
    """
    """

    total = 0

    for y in arena:
        for x in y:
            if x == 6:
                
                total += 1

    return total

def chaseClosestFood(myHead: dict, foodPos: dict, preferredMoves: list):
    """
    """

    closestFood = {"x": None, "y": None}
    smallestDistance = 99999999999999999999
    distance = 0

    # calculate the distance of all the food
    for food in foodPos:
        distance = abs(food["x"] - myHead["x"]) + abs(food["y"] - myHead["y"])
        if distance < smallestDistance:
            smallestDistance = distance
            closestFood["x"] = food["x"]
            closestFood["y"] = food["y"]

        print("d = " + str(distance))

    print("Closest food is: " + str(closestFood))

    if myHead["x"] - closestFood["x"] < 0:
        preferredMoves.append("right")
    else:
        preferredMoves.append("left")

    if myHead["y"] - closestFood["y"] < 0:
        preferredMoves.append("up")
    else:
        preferredMoves.append("down")

    return preferredMoves

        


    

#def determineBestPath(arena: list, possibleMoves: list, megaShark: dict):
 #   """
  #  """

    # Variables to help determine best possible path
   # upMoves = 0
    #downMoves = 0
    #leftMoves = 0
    #rightMoves = 0
    #mostMoves = 0

    # if "up" in possibleMoves:
        # upMoves = countPath(floodFill(copy.deepcopy(arena), megaShark["head"]["x"], megaShark["head"]["y"] + 1))
    # if "down" in possibleMoves:
        # downMoves = countPath(floodFill(copy.deepcopy(arena), megaShark["head"]["x"], megaShark["head"]["y"] - 1))
    # if "left" in possibleMoves:
        # leftMoves = countPath(floodFill(copy.deepcopy(arena), megaShark["head"]["x"] - 1, megaShark["head"]["y"]))
    # if "right" in possibleMoves:
        # rightMoves = countPath(floodFill(copy.deepcopy(arena), megaShark["head"]["x"] + 1, megaShark["head"]["y"]))

    # Check which direction will lead to the most moves
    # mostMoves = max([upMoves, downMoves, leftMoves, rightMoves])

    # if "up" in possibleMoves:
        # if upMoves != mostMoves:
            # possibleMoves.remove("up")
    # if "down" in possibleMoves:
        # if downMoves != mostMoves:
            # possibleMoves.remove("down")
    # if "left" in possibleMoves:
        # if leftMoves != mostMoves:
            # possibleMoves.remove("left")
    # if "right" in possibleMoves:
        # if rightMoves != mostMoves:
            # possibleMoves.remove("right")
# 
    # return possibleMoves