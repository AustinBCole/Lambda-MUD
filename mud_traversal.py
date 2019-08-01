import requests
import time
import json

MOVE_ENDPOINT = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
INIT_ENDPOINT = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"

headers = { 'Authorization': 'token 72835a1eadb9d32cc63af8173e157b0a1a4ff7df',
    'content-type': 'application/json'}


def move(direction):
    #set up move request then send
    move_data = {"direction": direction}
    data_json = json.dumps(move_data)
    r = requests.post(url=MOVE_ENDPOINT, data=data_json, headers=headers)
    #get return values
    #return values
    return r.json()

def wait(cooldown):
    time.sleep(cooldown)

def current_room_info():
    #set up get request then send
    r = requests.get(url=INIT_ENDPOINT, headers=headers)
    #get return values
    #return values
    return r.json()

def get_exits(current_room):
    exits_dictionary = {current_room["room_id"]: {}}
    exits = current_room["exits"]
    for exit in exits:
        exits_dictionary[current_room["room_id"]][exit] = "?"
    return exits_dictionary


next_direction = "?"


def traversal_algo():
    # declare opposites dic property
    opposites_dict = {
        "n": "s",
        "e":"w",
        "w":"e",
        "s":"n"
    }
    # Declare current room property
    current_room = current_room_info()
    time.sleep(current_room["cooldown"])

    current_room_id = current_room["room_id"]

    adjacency_list = get_exits(current_room)

    # Declare reverse traversal path variable
    reversed_traversal_path = []
    # Declare traversal path variable
    traversal_path = []
    # while length of visited is less than number of rooms
    while len(adjacency_list.keys()) < 500:
        print(len(adjacency_list.keys()))
        # get valid exits
        if current_room_id in adjacency_list:
            valid_exits_dict =  adjacency_list[current_room_id]
        else:
            valid_exits_dict = get_exits(current_room)[current_room_id]
        #get room info
        # get exits without question marks
        if "?" in valid_exits_dict.values():
            # Iterate over possible directions in current room exits
            for direction in valid_exits_dict.keys():
                # Move the player to that room and get room
                if valid_exits_dict[direction] == "?":
                    last_room_id = current_room_id
                    current_room = move(direction)
                    current_room_id = current_room["room_id"]
                    exits = get_exits(current_room)
                    if current_room_id not in adjacency_list:
                        adjacency_list.update(exits)
                    adjacency_list[current_room_id][opposites_dict[direction]] =last_room_id
                    adjacency_list[last_room_id][direction] = current_room_id
                    # Append traversalPath list with direction
                    traversal_path.append(direction)
                    # append to reverse_traversal path the opposite direction
                    reversed_traversal_path.append(opposites_dict[direction])
                    time.sleep(current_room["cooldown"])
                    break
        else:
            direction = reversed_traversal_path.pop()
            current_room = move(direction)
            current_room_id = current_room["room_id"]

            time.sleep(current_room["cooldown"])
            traversal_path.append(direction)
    return adjacency_list

    

map = traversal_algo()
with open ('mud_traversal_data.txt', 'w') as outfile:
    json.dump(map, outfile)
