from flask import Flask, request
import logic, os

app = Flask(__name__)

@app.get("/")
def registerSnake():
    """
    This function is only called when registering snake
    """
    print("INFO")
    return logic.getInfo()

@app.post("/start")
def deployShark():
    """
    This function is called every time MegaShark enters a game
    """
    data = request.get_json()
    print(f"{data['game']['id']} START")
    return "MegaShark has been deployed!"

@app.post("/move")
def make_move():
    """
    This is called every turn
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    print(data)
    move = logic.chooseMove(data)

    return {"move": move}

@app.post("/end")
def handle_end():
    """
    This function is called when a game your Battlesnake was in has ended.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()

    print(f"{data['game']['id']} END")
    return "ok"

if __name__ == "__main__":
    host = "0.0.0.0:$PORT"
    #port = int(os.environ.get("PORT", "8080"))

    # print(f"\nRunning Battlesnake server at http://{host}:{port}")
    app.run(host=host, debug=False)
    #app.run()