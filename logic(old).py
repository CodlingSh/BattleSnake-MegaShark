import random

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

    # Snake info
    my_snake = data["you"] # A dictionary with info about my snake
    enemy_snakes = data["board"]["snakes"] # A dictionary with info about enemy snakes
    food_locations = data["board"]["food"] # A dictionary with the coordinates for food
    my_head = my_snake["head"] # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"] # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]

    # Arena info
    arena_dimensions = [data["board"]["height"], data["board"]["height"]]

    possible_moves = ["up", "down", "left", "right"]
    preferred_move = ""

    # determine the closest piece of food and go for it.
    if len(food_locations) != 0:
      preferred_move = get_food(my_head, food_locations)

    # Make sure snake doesn't go back on itself and crash with it's neck
    possible_moves = avoid_neck(my_body, possible_moves)

    # Check for walls
    possible_moves = avoid_walls(my_head, arena_dimensions, possible_moves)

    # Check for snakes body
    possible_moves = avoid_self(my_body, possible_moves)

    # Check for enemy snakes
    possible_moves = avoid_enemies(my_body, enemy_snakes, possible_moves)

    if len(possible_moves) != 0:
      if preferred_move in possible_moves:
        my_move = preferred_move
      else:
        my_move = random.choice(possible_moves)    
    else:
      return "dead"
    
    print("Preferred Move: " + str(preferred_move))
    print("Possible Moves: " + str(possible_moves))
    print("Final Move: " + str(my_move))

    #print(str(my_head) + " Possible moves: " + str(possible_moves))
    return my_move#random.choice(possible_moves) 

def avoid_neck(my_body: dict, possible_moves: list):
  """
    my_body: Co-ordinates for the snakes body

    possible_moves: A list of all possible directions the snake can go in (up, down, left, right)

    return: An updated list of directions with the direction directly behind the snakes head removed
  """

  head = my_body[0]
  neck = my_body[1]

  # Check horizontal movement
  if head["x"] > neck["x"]:
    possible_moves.remove("left")
  elif head["x"] < neck["x"]:
    possible_moves.remove("right")

  # Check vertical movement
  if head["y"] > neck["y"]:
    possible_moves.remove("down")
  elif head["y"] < neck["y"]:
    possible_moves.remove("up")
  
  return possible_moves

def avoid_walls(my_head: dict, arena_size: list, possible_moves: list):
  """
    my_head: Co-ordinates for the snakes head

    arena_size: The width and height of the arena

    return: An updated list of directions with the direction that will hit a wall removed
  """

  if my_head["x"] == 0:
    if "left" in possible_moves:
            possible_moves.remove("left")
  if my_head["x"] == arena_size[0] - 1:
    if "right" in possible_moves:
            possible_moves.remove("right")
  if my_head["y"] == 0:
    if "down" in possible_moves:
            possible_moves.remove("down")
  if my_head["y"] == arena_size[1] - 1:
    if "up" in possible_moves:
            possible_moves.remove("up")
  
  return possible_moves

def avoid_self(my_body: dict, possible_moves: list):
  """
  """
  
  my_head = my_body[0]
  left_dir = {"x": my_head["x"] - 1, "y": my_head["y"]}
  right_dir = {"x": my_head["x"] + 1, "y": my_head["y"]}
  up_dir = {"x": my_head["x"], "y": my_head["y"] + 1}
  down_dir = {"x": my_head["x"], "y": my_head["y"] - 1}

  for i in my_body[1:]:
    #print(i)
    #print(left_dir == i)
    if left_dir == i:
        if "left" in possible_moves:
            possible_moves.remove("left")
    if right_dir == i:
        if "right" in possible_moves:
            possible_moves.remove("right")
    if up_dir == i:
        if "up" in possible_moves:
            possible_moves.remove("up")
    if down_dir == i:
        if "down" in possible_moves:
            possible_moves.remove("down")

  return possible_moves

def avoid_enemies(my_body: dict, enemies: dict, possible_moves: list):
  """
  """

  my_head = my_body[0]
  left_dir = {"x": my_head["x"] - 1, "y": my_head["y"]}
  right_dir = {"x": my_head["x"] + 1, "y": my_head["y"]}
  up_dir = {"x": my_head["x"], "y": my_head["y"] + 1}
  down_dir = {"x": my_head["x"], "y": my_head["y"] - 1}

  # Check where snakes are
  for snake in enemies:
    if left_dir in snake["body"]:
        if "left" in possible_moves:
            possible_moves.remove("left")
    if right_dir in snake["body"]:
        if "right" in possible_moves:
            possible_moves.remove("right")
    if up_dir in snake["body"]:
        if "up" in possible_moves:
            possible_moves.remove("up")
    if down_dir in snake["body"]:
        if "down" in possible_moves:
            possible_moves.remove("down")

  return possible_moves

def get_food(my_head: dict, food: dict):
  """
  """

  preferred_moves = []
  closest_food = {"x": None, "y": None}
  distance = 100000000

  for food_piece in food:
    if ((my_head["x"] - food_piece["x"]) + (my_head["y"] - food_piece["y"])) < distance:
      closest_food["x"] = food_piece["x"]
      closest_food["y"] = food_piece["y"]
      distance = (my_head["x"] - food_piece["x"]) + (my_head["y"] - food_piece["y"])

  if my_head["x"] - closest_food["x"] > 0:
    preferred_moves.append("left")
  elif my_head["x"] - closest_food["x"] < 0:
    preferred_moves.append("right")

  if my_head["y"] - closest_food["y"] > 0:
    preferred_moves.append("down")
  elif my_head["y"] - closest_food["y"] < 0:
    preferred_moves.append("up")

  print("Closest Food: " + str(closest_food))
  print("Preferred Moves: " + str(preferred_moves))

  if len(preferred_moves) == 0:
    return "No preferred move"

  return random.choice(preferred_moves)




  