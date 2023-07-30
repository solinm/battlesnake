import random
from typing import List, Dict

def get_info() -> dict:
    return {
        "apiversion": "1",
        "author": "solin",
        "color": "#88CEED",
        "head": "snail",
        "tail": "snail",
    }

def choose_move(data: dict) -> str:
    my_snake = data["you"]
    my_head = my_snake["head"]
    my_body = {segment["x"]: segment["y"] for segment in my_snake["body"]}  
    board = data['board']
    board_height = board['height']
    board_width = board['width']
    max_height = board_height - 1
    max_width = board_width - 1

    possible_moves = {"up", "down", "left", "right"} 

    # Step 0: Don't allow your Battlesnake to move back on its own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # Step 1: Don't hit walls.
    possible_moves = _avoid_the_walls(max_height, max_width, my_head, possible_moves)

    # Step 2: Don't hit yourself.
    possible_moves = _avoid_self_collision(my_head, my_body, possible_moves)

    # Step 3: Don't collide with others.
    other_snakes = {snake["id"]: {segment["x"]: segment["y"] for segment in snake["body"]} for snake in data["board"]["snakes"] if snake["id"] != my_snake["id"]}
    possible_moves = _avoid_other_snakes_collision(my_head, other_snakes, possible_moves)

    # Step 4: Find food and choose the best move
    if possible_moves:
        move = random.choice(list(possible_moves))
    else:
        move = random.choice(["up", "down", "left", "right"])

    return move

def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    my_head = my_body[0] 
    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.discard("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.discard("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.discard("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.discard("up")

    return possible_moves

def _avoid_the_walls(max_height: int, max_width: int, my_head: Dict, possible_moves: List[str]) -> List[str]:
    if my_head["x"] == max_width:
        possible_moves.discard("right")
    elif my_head["x"] == 0:
        possible_moves.discard("left")

    if my_head["y"] == max_height:
        possible_moves.discard("up")
    elif my_head["y"] == 0:
        possible_moves.discard("down")

    return possible_moves

def _avoid_self_collision(my_head, my_body, possible_moves):
    next_heads = {
        "up": {"x": my_head["x"], "y": my_head["y"] + 1},
        "down": {"x": my_head["x"], "y": my_head["y"] - 1},
        "left": {"x": my_head["x"] - 1, "y": my_head["y"]},
        "right": {"x": my_head["x"] + 1, "y": my_head["y"]}
    }

    possible_moves = {move for move in possible_moves if next_heads[move] not in my_body.values()}

    return possible_moves

def _avoid_other_snakes_collision(my_head, other_snakes, possible_moves):
    next_heads = {
        "up": {"x": my_head["x"], "y": my_head["y"] + 1},
        "down": {"x": my_head["x"], "y": my_head["y"] - 1},
        "left": {"x": my_head["x"] - 1, "y": my_head["y"]},
        "right": {"x": my_head["x"] + 1, "y": my_head["y"]}
    }

    for move in possible_moves.copy():
        new_head = next_heads[move]
        for snake_body in other_snakes.values():
            if new_head in snake_body.values():
                possible_moves.discard(move)
                break

    return possible_moves